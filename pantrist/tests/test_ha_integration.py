import httpx
import pytest
import respx

from ha_integration import HAClient


@respx.mock
def test_post_persistent_notification_calls_supervisor_endpoint(monkeypatch):
    monkeypatch.setenv("SUPERVISOR_TOKEN", "test-token")
    route = respx.post(
        "http://supervisor/core/api/services/persistent_notification/create"
    ).mock(return_value=httpx.Response(200, json={}))
    client = HAClient()
    client.post_persistent_notification(
        notification_id="pantrist_reauth",
        title="Pantrist",
        message="Reconnect needed",
    )
    assert route.called
    request = route.calls.last.request
    assert request.headers["Authorization"] == "Bearer test-token"
    import json
    body = json.loads(request.content)
    assert body == {
        "notification_id": "pantrist_reauth",
        "title": "Pantrist",
        "message": "Reconnect needed",
    }


@respx.mock
def test_post_persistent_notification_swallows_errors(monkeypatch, caplog):
    monkeypatch.setenv("SUPERVISOR_TOKEN", "test-token")
    respx.post(
        "http://supervisor/core/api/services/persistent_notification/create"
    ).mock(return_value=httpx.Response(500))
    client = HAClient()
    # Must NOT raise — caller may be inside a critical loop
    client.post_persistent_notification(
        notification_id="pantrist_reauth",
        title="Pantrist",
        message="Reconnect needed",
    )
    # Error was logged
    assert any("post_persistent_notification" in r.message.lower() or "500" in r.message for r in caplog.records)
