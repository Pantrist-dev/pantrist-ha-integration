"""Socket.IO listener for real-time Pantrist updates.

Connects to the Pantrist /lists Socket.IO namespace, joins the active
shopping-list and pantry rooms, and invokes callbacks whenever data changes.
The caller is responsible for re-fetching full list data via REST on each
callback invocation.

Handled collections:
  shoppingList, shoppingList:itemAdded/Updated/Removed
  pantryList,   pantryList:itemAdded/Updated/Removed
  shoppingCart, shoppingCart:itemAdded/Updated/Removed
"""

import logging
import threading
from typing import Callable

import socketio

logger = logging.getLogger(__name__)

OnListEventFn = Callable[[str], None]  # receives listId

_NAMESPACE = "/lists"
_MAX_BACKOFF = 60

_SHOPPING_COLLECTIONS = frozenset({
    "shoppingList",
    "shoppingList:itemAdded",
    "shoppingList:itemUpdated",
    "shoppingList:itemRemoved",
})
_PANTRY_COLLECTIONS = frozenset({
    "pantryList",
    "pantryList:itemAdded",
    "pantryList:itemUpdated",
    "pantryList:itemRemoved",
})
_CART_COLLECTIONS = frozenset({
    "shoppingCart",
    "shoppingCart:itemAdded",
    "shoppingCart:itemUpdated",
    "shoppingCart:itemRemoved",
})


class PantristSocketIOListener:
    """Maintains a Socket.IO connection and calls back on list mutations."""

    def __init__(
        self,
        base_url: str,
        token: str,
        shopping_list_id: str,
        pantry_list_id: str,
        on_shopping_updated: OnListEventFn,
        on_pantry_updated: OnListEventFn,
        on_shopping_cart_updated: OnListEventFn,
    ) -> None:
        self._base_url = base_url
        self._token = token
        self._shopping_list_id = shopping_list_id
        self._pantry_list_id = pantry_list_id
        self._on_shopping = on_shopping_updated
        self._on_pantry = on_pantry_updated
        self._on_cart = on_shopping_cart_updated
        self._stop = threading.Event()
        self._sio: socketio.Client | None = None
        self._thread = threading.Thread(
            target=self._run, daemon=True, name="pantrist-sio"
        )

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        self._disconnect()

    def update_token(self, token: str) -> None:
        """Update the auth token and force a reconnect so the new token is used."""
        self._token = token
        logger.info("Token updated — forcing Socket.IO reconnect")
        self._disconnect()

    def update_list_ids(self, new_shopping_id: str, new_pantry_id: str) -> None:
        """Switch to a different active list, leaving old rooms and joining new ones."""
        old_shopping = self._shopping_list_id
        old_pantry = self._pantry_list_id
        self._shopping_list_id = new_shopping_id
        self._pantry_list_id = new_pantry_id

        sio = self._sio
        if sio is None or not sio.connected:
            return  # reconnect will join the correct rooms

        if old_shopping and old_shopping != new_shopping_id:
            sio.emit("leaveList", {"listId": old_shopping}, namespace=_NAMESPACE)
            logger.info("Left old shopping list room: %s", old_shopping)
        if old_pantry and old_pantry != new_pantry_id:
            sio.emit("leaveList", {"listId": old_pantry}, namespace=_NAMESPACE)
            logger.info("Left old pantry room: %s", old_pantry)

        if new_shopping_id and new_shopping_id != old_shopping:
            sio.emit("joinList", {"listId": new_shopping_id}, namespace=_NAMESPACE)
            logger.info("Joined new shopping list room: %s", new_shopping_id)
        if new_pantry_id and new_pantry_id != old_pantry:
            sio.emit("joinList", {"listId": new_pantry_id}, namespace=_NAMESPACE)
            logger.info("Joined new pantry room: %s", new_pantry_id)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _disconnect(self) -> None:
        sio = self._sio
        if sio is not None and sio.connected:
            try:
                sio.disconnect()
            except Exception:
                pass

    def _run(self) -> None:
        backoff = 2
        while not self._stop.is_set():
            try:
                self._connect_and_wait()
                backoff = 2
            except Exception:
                logger.exception("Socket.IO connection failed")
            if not self._stop.is_set():
                logger.info("Reconnecting in %d s…", backoff)
                self._stop.wait(timeout=backoff)
                backoff = min(backoff * 2, _MAX_BACKOFF)

    def _connect_and_wait(self) -> None:
        sio = socketio.Client(logger=False, engineio_logger=False)
        self._sio = sio

        @sio.event(namespace=_NAMESPACE)
        def connect():
            logger.info("Socket.IO connected to %s%s", self._base_url, _NAMESPACE)
            for list_id in (self._shopping_list_id, self._pantry_list_id):
                if list_id:
                    sio.emit("joinList", {"listId": list_id}, namespace=_NAMESPACE)
                    logger.debug("Joined list room: %s", list_id)

        @sio.event(namespace=_NAMESPACE)
        def connect_error(data):
            logger.error("Socket.IO connect error: %s", data)

        @sio.event(namespace=_NAMESPACE)
        def disconnect():
            logger.info("Socket.IO disconnected")

        @sio.on("data:updated", namespace=_NAMESPACE)
        def on_data_updated(data):
            collection = data.get("collection", "")
            list_id = data.get("listId", "")
            if collection in _SHOPPING_COLLECTIONS:
                logger.debug("Shopping list event '%s' for %s", collection, list_id)
                try:
                    self._on_shopping(list_id)
                except Exception:
                    logger.exception("on_shopping_updated callback failed")
            elif collection in _PANTRY_COLLECTIONS:
                logger.debug("Pantry event '%s' for %s", collection, list_id)
                try:
                    self._on_pantry(list_id)
                except Exception:
                    logger.exception("on_pantry_updated callback failed")
            elif collection in _CART_COLLECTIONS:
                logger.debug("Shopping cart event '%s' for %s", collection, list_id)
                try:
                    self._on_cart(list_id)
                except Exception:
                    logger.exception("on_shopping_cart_updated callback failed")

        sio.connect(
            self._base_url,
            namespaces=[_NAMESPACE],
            auth={"token": self._token},
            transports=["websocket"],
        )
        try:
            sio.wait()
        finally:
            self._sio = None
            if sio.connected:
                try:
                    sio.disconnect()
                except Exception:
                    pass
