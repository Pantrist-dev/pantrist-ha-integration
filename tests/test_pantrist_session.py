import sys
import types
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Stub the generated pantrist_client package so pantrist_api can be imported
# without the generated OpenAPI code being present.
# ---------------------------------------------------------------------------
def _make_stub_module(name: str) -> types.ModuleType:
    """Return a real ModuleType whose attributes fall back to MagicMock."""

    class _StubModule(types.ModuleType):
        def __getattr__(self, item: str) -> MagicMock:
            value = MagicMock()
            object.__setattr__(self, item, value)
            return value

    mod = _StubModule(name)
    mod.__path__ = []  # type: ignore[attr-defined]  # marks it as a package
    return mod


for _name in [
    "pantrist_client",
    "pantrist_client.api",
    "pantrist_client.api.barcode",
    "pantrist_client.api.list",
    "pantrist_client.api.pantry_list",
    "pantrist_client.api.pantry_list_items",
    "pantrist_client.api.shopping_cart",
    "pantrist_client.api.shopping_list",
    "pantrist_client.models",
]:
    sys.modules.setdefault(_name, _make_stub_module(_name))

from credentials import Credentials


@patch("pantrist_session.PantristAPI")
@patch("pantrist_session.PantristSocketIOListener")
@patch("pantrist_session.TokenManager")
def test_start_then_stop_idempotent(token_mgr_cls, sio_cls, api_cls):
    from pantrist_session import PantristSession

    token_mgr_cls.return_value.access_token = "at-1"
    api_cls.return_value.get_shopping_list.return_value = {}
    api_cls.return_value.get_pantry_list.return_value = {}
    api_cls.return_value.get_shopping_cart.return_value = []

    ha_client = MagicMock()
    session = PantristSession(
        socket_url="https://api.example",
        expiry_warning_days=7,
        ha_client=ha_client,
    )
    creds = Credentials(refresh_token="rt", list_id="list-1")

    assert session.is_running is False
    session.start(creds)
    assert session.is_running is True

    # Second start while already running is a no-op
    session.start(creds)
    api_cls.assert_called_once()
    token_mgr_cls.assert_called_once()

    session.stop()
    assert session.is_running is False

    # Stop while already stopped is a no-op
    session.stop()


@patch("pantrist_session.PantristAPI")
@patch("pantrist_session.PantristSocketIOListener")
@patch("pantrist_session.TokenManager")
def test_token_failure_callback_stops_session_and_notifies(token_mgr_cls, sio_cls, api_cls):
    from pantrist_session import PantristSession

    token_mgr_cls.return_value.access_token = "at-1"
    api_cls.return_value.get_shopping_list.return_value = {}
    api_cls.return_value.get_pantry_list.return_value = {}
    api_cls.return_value.get_shopping_cart.return_value = []

    ha_client = MagicMock()
    session = PantristSession(
        socket_url="https://api.example",
        expiry_warning_days=7,
        ha_client=ha_client,
    )
    session.start(Credentials(refresh_token="rt", list_id="list-1"))

    # Grab the on_failure callback the session passed to TokenManager
    call_kwargs = token_mgr_cls.call_args.kwargs
    on_failure = call_kwargs.get("on_failure")
    assert on_failure is not None
    on_failure()

    ha_client.post_persistent_notification.assert_called_once()
    args, kwargs = ha_client.post_persistent_notification.call_args
    assert kwargs.get("notification_id") == "pantrist_reauth" or "pantrist_reauth" in args
    assert session.is_running is False


@patch("pantrist_session.PantristAPI")
@patch("pantrist_session.PantristSocketIOListener")
@patch("pantrist_session.TokenManager")
def test_start_populates_sensors_with_chosen_list(token_mgr_cls, sio_cls, api_cls):
    from pantrist_session import PantristSession

    token_mgr_cls.return_value.access_token = "at-1"
    api_cls.return_value.get_shopping_list.return_value = {"items": []}
    api_cls.return_value.get_pantry_list.return_value = {"items": []}
    api_cls.return_value.get_shopping_cart.return_value = []

    ha_client = MagicMock()
    session = PantristSession(
        socket_url="https://api.example",
        expiry_warning_days=7,
        ha_client=ha_client,
    )
    session.start(Credentials(refresh_token="rt", list_id="list-1"))

    # Initial fetch called with the chosen list_id (NOT current-list endpoint)
    api_cls.return_value.get_shopping_list.assert_called_with("list-1")
    api_cls.return_value.get_pantry_list.assert_called_with("list-1")
    api_cls.return_value.get_shopping_cart.assert_called_with("list-1")
