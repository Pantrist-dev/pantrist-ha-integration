"""
Pantrist Home Assistant Addon

Connects to the Pantrist Socket.IO server for real-time updates and pushes
them into HA as sensor states. Also runs a local HTTP server so HA can call
mutating Pantrist actions via rest_command.

Sensor entities:
  sensor.pantrist_shopping_list  – item count + items attribute
  sensor.pantrist_pantry         – item count + items / low_stock attributes
  sensor.pantrist_expiring_soon  – count of items expiring within warning window
  sensor.pantrist_shopping_cart  – items in the intermediate shopping cart

HTTP service endpoints (POST, JSON body):
  /services/add_to_shopping_list             { "name": "Milk" }
  /services/add_to_shopping_list_by_barcode  { "barcode": "4006381333931" }
  /services/add_to_pantry                    { "name": "Milk", "amount": 2,
                                               "unit_id": "pieces" }
  /services/check_shopping_list_item         { "item_id": "<uuid>" }
  /services/delete_shopping_list_item        { "list_id": "<id>", "item_id": "<uuid>" }
  /services/delete_pantry_item               { "list_id": "<id>", "item_id": "<uuid>" }
  /services/change_pantry_item_amount        { "list_id": "<id>", "item_id": "<uuid>",
                                               "change": -1, "unit_id": "pieces" }
  /health                                    (GET) {"status":"ok"}
"""

import json
import logging
import signal
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from ha_integration import (
    HAClient,
    build_expiring_soon_state,
    build_pantry_state,
    build_shopping_cart_state,
    build_shopping_list_state,
)
from pantrist_api import PantristAPI
from socketio_listener import PantristSocketIOListener
from token_manager import TokenManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("pantrist_addon")

CONFIG_PATH = "/data/options.json"
SERVICE_PORT = 8099
LIST_POLL_INTERVAL = 300  # seconds between active-list checks


def load_config() -> dict:
    with open(CONFIG_PATH) as fh:
        return json.load(fh)


# ---------------------------------------------------------------------------
# HTTP service server
# ---------------------------------------------------------------------------


def _json_body(request: BaseHTTPRequestHandler) -> dict:
    length = int(request.headers.get("Content-Length", 0))
    raw = request.rfile.read(length) if length else b"{}"
    return json.loads(raw)


def _send_json(request: BaseHTTPRequestHandler, status: int, body: dict) -> None:
    data = json.dumps(body).encode()
    request.send_response(status)
    request.send_header("Content-Type", "application/json")
    request.send_header("Content-Length", str(len(data)))
    request.end_headers()
    request.wfile.write(data)


class _ServiceHandler(BaseHTTPRequestHandler):
    api: PantristAPI

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/health":
            _send_json(self, 200, {"status": "ok"})
        else:
            _send_json(self, 404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        try:
            body = _json_body(self)
            result = self._dispatch(body)
            _send_json(self, 200, result if result is not None else {"success": True})
        except KeyError as exc:
            _send_json(self, 400, {"error": f"Missing field: {exc}"})
        except Exception as exc:
            logger.exception("Service call to %s failed", self.path)
            _send_json(self, 500, {"error": str(exc)})

    def _dispatch(self, body: dict) -> dict | None:
        path = self.path

        if path == "/services/add_to_shopping_list":
            return self.api.add_to_shopping_list_by_name(body["name"])

        if path == "/services/add_to_shopping_list_by_barcode":
            return self.api.add_to_shopping_list_by_barcode(body["barcode"])

        if path == "/services/add_to_pantry":
            return self.api.add_to_pantry_by_name(
                body["name"],
                float(body.get("amount", 1)),
                body.get("unit_id", "pieces"),
            )

        if path == "/services/check_shopping_list_item":
            self.api.check_shopping_list_item(body["item_id"])
            return None

        if path == "/services/delete_shopping_list_item":
            self.api.delete_shopping_list_item(body["list_id"], body["item_id"])
            return None

        if path == "/services/delete_pantry_item":
            self.api.delete_pantry_item(body["list_id"], body["item_id"])
            return None

        if path == "/services/change_pantry_item_amount":
            return self.api.change_pantry_item_amount(
                body["list_id"],
                body["item_id"],
                float(body["change"]),
                body["unit_id"],
            )

        _send_json(self, 404, {"error": "unknown service endpoint"})
        return None

    def log_message(self, fmt: str, *args) -> None:  # noqa: D401
        logger.debug("HTTP %s", fmt % args)


def make_handler_factory(api: PantristAPI):
    class BoundHandler(_ServiceHandler):
        pass

    BoundHandler.api = api
    return BoundHandler


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> None:
    config = load_config()
    api_token: str = (config.get("api_token") or "").strip()
    refresh_token: str = (config.get("refresh_token") or "").strip()
    socket_url: str = config["socket_url"]
    expiry_warning_days: int = int(config.get("expiry_warning_days", 7))

    if not api_token and not refresh_token:
        logger.error("Either api_token or refresh_token must be configured.")
        sys.exit(1)
    if not socket_url:
        logger.error("socket_url is not configured.")
        sys.exit(1)

    # ------------------------------------------------------------------
    # Auth: use OAuth refresh flow when refresh_token is provided,
    # otherwise fall back to a static Firebase ID token.
    # ------------------------------------------------------------------
    token_manager: TokenManager | None = None

    if refresh_token:
        token_manager = TokenManager(
            refresh_token=refresh_token,
            on_token_updated=lambda t: None,  # callbacks wired below after objects exist
        )
        logger.info("Starting with OAuth refresh token — performing initial refresh…")
        token_manager.start()
        active_token = token_manager.access_token
        logger.info("Initial access token obtained.")
    else:
        logger.warning(
            "Using static api_token — it expires in ~1 hour. "
            "Configure refresh_token for automatic renewal."
        )
        active_token = api_token

    api = PantristAPI(active_token)
    ha = HAClient()

    # ------------------------------------------------------------------
    # Initial data fetch — populate all sensors and capture list IDs
    # ------------------------------------------------------------------
    def _fetch_shopping(list_id: str | None = None) -> tuple[str, str, dict]:
        data = api.get_shopping_list(list_id) if list_id else api.get_current_shopping_list()
        s, a = build_shopping_list_state(data)
        ha.set_state("sensor.pantrist_shopping_list", s, a)
        return a.get("list_id", ""), s, a

    def _fetch_pantry(list_id: str | None = None) -> tuple[str, str, dict]:
        data = api.get_pantry_list(list_id) if list_id else api.get_current_pantry_list()
        s, a = build_pantry_state(data)
        ha.set_state("sensor.pantrist_pantry", s, a)
        es, ea = build_expiring_soon_state(data, expiry_warning_days)
        ha.set_state("sensor.pantrist_expiring_soon", es, ea)
        return a.get("list_id", ""), s, a

    def _fetch_cart(list_id: str | None = None) -> tuple[str, dict]:
        data = api.get_shopping_cart()
        s, a = build_shopping_cart_state(data)
        ha.set_state("sensor.pantrist_shopping_cart", s, a)
        return s, a

    try:
        shopping_list_id, s, _ = _fetch_shopping()
        logger.info("Initial shopping list: %s items (id=%s)", s, shopping_list_id)
    except Exception:
        logger.exception("Failed to fetch initial shopping list")
        shopping_list_id = ""

    try:
        pantry_list_id, s, _ = _fetch_pantry()
        logger.info("Initial pantry: %s items (id=%s)", s, pantry_list_id)
    except Exception:
        logger.exception("Failed to fetch initial pantry list")
        pantry_list_id = ""

    try:
        s, _ = _fetch_cart()
        logger.info("Initial shopping cart: %s items", s)
    except Exception:
        logger.exception("Failed to fetch initial shopping cart")

    # Track current list IDs so the poll thread can detect switches.
    current_ids: dict[str, str] = {
        "shopping": shopping_list_id,
        "pantry": pantry_list_id,
    }

    # ------------------------------------------------------------------
    # Socket.IO callbacks
    # ------------------------------------------------------------------
    def on_shopping_updated(list_id: str) -> None:
        try:
            _fetch_shopping(list_id)
            logger.info("Shopping list updated")
        except Exception:
            logger.exception("Failed to refresh shopping list %s", list_id)

    def on_pantry_updated(list_id: str) -> None:
        try:
            _, s, a = _fetch_pantry(list_id)
            logger.info("Pantry updated: %s items (%s low stock)", s, a.get("low_stock_count"))
        except Exception:
            logger.exception("Failed to refresh pantry %s", list_id)

    def on_cart_updated(_list_id: str) -> None:
        try:
            s, _ = _fetch_cart()
            logger.info("Shopping cart updated: %s items", s)
        except Exception:
            logger.exception("Failed to refresh shopping cart")

    sio_listener = PantristSocketIOListener(
        base_url=socket_url,
        token=active_token,
        shopping_list_id=shopping_list_id,
        pantry_list_id=pantry_list_id,
        on_shopping_updated=on_shopping_updated,
        on_pantry_updated=on_pantry_updated,
        on_shopping_cart_updated=on_cart_updated,
    )
    sio_listener.start()

    # Wire token refresh into API + Socket.IO after both objects exist.
    if token_manager is not None:
        def _on_token_updated(new_token: str) -> None:
            api.update_token(new_token)
            sio_listener.update_token(new_token)

        token_manager._on_token_updated = _on_token_updated  # noqa: SLF001

    # ------------------------------------------------------------------
    # List-switching poll — re-join rooms when the user switches lists
    # ------------------------------------------------------------------
    stop_poll = threading.Event()

    def _list_poll() -> None:
        while not stop_poll.wait(timeout=LIST_POLL_INTERVAL):
            try:
                new_shopping_id, _, _ = _fetch_shopping()
                new_pantry_id, _, _ = _fetch_pantry()
                if (
                    new_shopping_id != current_ids["shopping"]
                    or new_pantry_id != current_ids["pantry"]
                ):
                    logger.info(
                        "Active list changed (shopping: %s→%s, pantry: %s→%s) — rejoining rooms",
                        current_ids["shopping"], new_shopping_id,
                        current_ids["pantry"], new_pantry_id,
                    )
                    current_ids["shopping"] = new_shopping_id
                    current_ids["pantry"] = new_pantry_id
                    sio_listener.update_list_ids(new_shopping_id, new_pantry_id)
            except Exception:
                logger.exception("List poll failed")

    poll_thread = threading.Thread(target=_list_poll, daemon=True, name="pantrist-list-poll")
    poll_thread.start()

    # ------------------------------------------------------------------
    # HTTP server for mutating service calls
    # ------------------------------------------------------------------
    server = HTTPServer(("0.0.0.0", SERVICE_PORT), make_handler_factory(api))
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    logger.info("Service server listening on port %d", SERVICE_PORT)

    def _shutdown(sig, _frame) -> None:
        logger.info("Shutting down (signal %s)…", sig)
        stop_poll.set()
        sio_listener.stop()
        if token_manager is not None:
            token_manager.stop()
        server.shutdown()
        api.close()
        ha.close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)

    logger.info("Pantrist addon running (Socket.IO mode)")
    signal.pause()


if __name__ == "__main__":
    main()
