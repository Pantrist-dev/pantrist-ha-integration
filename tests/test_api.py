"""PantristApi wrapper tests."""

from __future__ import annotations

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from custom_components.pantrist.api import (
    PantristApi,
    PantristApiError,
    PantristAuthError,
)

LIST_ID = "00000000-0000-4000-8000-000000000001"


@pytest.fixture
def api() -> PantristApi:
    """An API wrapper with a stubbed OAuth2 session — no real HA needed."""
    hass = MagicMock()
    session = MagicMock()
    session.async_ensure_token_valid = AsyncMock()
    session.token = {"access_token": "tok"}
    return PantristApi(hass, session)


async def test_client_refreshes_token(api: PantristApi) -> None:
    client = await api._client()
    session: Any = api._session
    session.async_ensure_token_valid.assert_awaited_once()
    assert client.token == "tok"


def test_wrap_passthrough_for_plain_types() -> None:
    assert PantristApi._wrap(None) is None
    assert PantristApi._wrap(42) == 42
    assert PantristApi._wrap({"k": "v"}) == {"k": "v"}


def test_wrap_calls_to_dict() -> None:
    obj = MagicMock()
    obj.to_dict.return_value = {"x": 1}
    assert PantristApi._wrap(obj) == {"x": 1}


def test_wrap_lists() -> None:
    a = MagicMock()
    a.to_dict.return_value = {"i": 1}
    b = MagicMock(spec=[])  # no to_dict
    assert PantristApi._wrap([a, b]) == [{"i": 1}, b]


async def test_call_returns_result(api: PantristApi) -> None:
    async def _coro():
        return "ok"

    assert await api._call(_coro()) == "ok"


async def test_call_translates_401(api: PantristApi) -> None:
    response = httpx.Response(401, text="nope")
    request = httpx.Request("GET", "http://x")
    response._request = request

    async def _raises():
        raise httpx.HTTPStatusError("401", request=request, response=response)

    with pytest.raises(PantristAuthError):
        await api._call(_raises())


async def test_call_translates_other_http_errors(api: PantristApi) -> None:
    response = httpx.Response(500, text="boom")
    request = httpx.Request("GET", "http://x")
    response._request = request

    async def _raises():
        raise httpx.HTTPStatusError("500", request=request, response=response)

    with pytest.raises(PantristApiError):
        await api._call(_raises())


async def test_call_translates_request_errors(api: PantristApi) -> None:
    async def _raises():
        raise httpx.ConnectError("dns")

    with pytest.raises(PantristApiError):
        await api._call(_raises())


def _make_dto(**fields):
    """Build a fake attrs-style DTO with a to_dict method."""
    dto = MagicMock()
    dto.to_dict.return_value = dict(fields)
    return dto


async def test_get_lists(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api.list_controller_get_list.asyncio",
        new=AsyncMock(return_value=[_make_dto(id=LIST_ID, name="Home")]),
    ):
        result = await api.get_lists()
    assert result == [{"id": LIST_ID, "name": "Home"}]


async def test_get_lists_empty(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api.list_controller_get_list.asyncio",
        new=AsyncMock(return_value=None),
    ):
        assert await api.get_lists() == []


async def test_get_shopping_list(api: PantristApi) -> None:
    items = [_make_dto(uuid="i1", name="Milk")]
    with patch(
        "custom_components.pantrist.api._shopping_get_items.asyncio",
        new=AsyncMock(return_value=items),
    ):
        result = await api.get_shopping_list(LIST_ID)
    assert result == {"listId": LIST_ID, "items": [{"uuid": "i1", "name": "Milk"}]}


async def test_get_shopping_list_empty(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api._shopping_get_items.asyncio",
        new=AsyncMock(return_value=None),
    ):
        result = await api.get_shopping_list(LIST_ID)
    assert result == {"listId": LIST_ID, "items": []}


async def test_add_to_shopping_list_by_name(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api.shopping_list_items_controller_add_by_name.asyncio",
        new=AsyncMock(return_value=_make_dto(uuid="i1")),
    ) as m:
        result = await api.add_to_shopping_list_by_name(LIST_ID, "Bananas")
    assert result == {"uuid": "i1"}
    m.assert_awaited_once()


async def test_add_to_shopping_list_by_name_returns_empty_dict_when_none(
    api: PantristApi,
) -> None:
    with patch(
        "custom_components.pantrist.api.shopping_list_items_controller_add_by_name.asyncio",
        new=AsyncMock(return_value=None),
    ):
        assert await api.add_to_shopping_list_by_name(LIST_ID, "Bananas") == {}


async def test_add_to_shopping_list_by_barcode(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api.shopping_list_items_controller_add_by_barcode.asyncio",
        new=AsyncMock(return_value=_make_dto(uuid="i1")),
    ):
        result = await api.add_to_shopping_list_by_barcode(LIST_ID, "12345")
    assert result == {"uuid": "i1"}


async def test_add_to_shopping_list_by_barcode_handles_none(
    api: PantristApi,
) -> None:
    with patch(
        "custom_components.pantrist.api.shopping_list_items_controller_add_by_barcode.asyncio",
        new=AsyncMock(return_value=None),
    ):
        assert await api.add_to_shopping_list_by_barcode(LIST_ID, "9") == {}


async def test_check_shopping_list_item(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api.shopping_list_items_controller_check_item.asyncio_detailed",
        new=AsyncMock(return_value=None),
    ) as m:
        await api.check_shopping_list_item(LIST_ID, "i1")
    m.assert_awaited_once()


async def test_delete_shopping_list_item(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api.shopping_list_items_controller_delete_item.asyncio_detailed",
        new=AsyncMock(return_value=None),
    ) as m:
        await api.delete_shopping_list_item(LIST_ID, "i1")
    m.assert_awaited_once()


async def test_get_pantry_list(api: PantristApi) -> None:
    items = [_make_dto(uuid="p1", name="Rice")]
    with patch(
        "custom_components.pantrist.api._pantry_get_items.asyncio",
        new=AsyncMock(return_value=items),
    ):
        result = await api.get_pantry_list(LIST_ID)
    assert result == {"listId": LIST_ID, "items": [{"uuid": "p1", "name": "Rice"}]}


async def test_get_pantry_list_empty(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api._pantry_get_items.asyncio",
        new=AsyncMock(return_value=None),
    ):
        assert await api.get_pantry_list(LIST_ID) == {"listId": LIST_ID, "items": []}


async def test_add_to_pantry_by_name(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api.pantry_list_items_controller_add_by_name.asyncio",
        new=AsyncMock(return_value=_make_dto(uuid="p1")),
    ):
        result = await api.add_to_pantry_by_name(LIST_ID, "Eggs", amount=12, unit_id="pieces")
    assert result == {"uuid": "p1"}


async def test_add_to_pantry_handles_none(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api.pantry_list_items_controller_add_by_name.asyncio",
        new=AsyncMock(return_value=None),
    ):
        assert await api.add_to_pantry_by_name(LIST_ID, "Eggs") == {}


async def test_delete_pantry_item(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api.pantry_list_items_controller_delete_item.asyncio_detailed",
        new=AsyncMock(return_value=None),
    ) as m:
        await api.delete_pantry_item(LIST_ID, "p1")
    m.assert_awaited_once()


async def test_change_pantry_item_amount(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api.pantry_list_items_controller_change_amount.asyncio",
        new=AsyncMock(return_value=_make_dto(uuid="p1", amount=2)),
    ):
        result = await api.change_pantry_item_amount(LIST_ID, "p1", change=-1)
    assert result == {"uuid": "p1", "amount": 2}


async def test_change_pantry_item_amount_with_extra_kwargs(api: PantristApi) -> None:
    """Optional kwargs (group/pantry id) thread through to the DTO."""
    with patch(
        "custom_components.pantrist.api.pantry_list_items_controller_change_amount.asyncio",
        new=AsyncMock(return_value=None),
    ) as m:
        result = await api.change_pantry_item_amount(
            LIST_ID, "p1", change=2, product_group_index=1.0, pantry_id="pantry-x"
        )
    assert result == {}
    m.assert_awaited_once()


async def test_get_shopping_cart(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api._cart_get_items.asyncio",
        new=AsyncMock(return_value=[_make_dto(uuid="c1")]),
    ):
        result = await api.get_shopping_cart(LIST_ID)
    assert result == [{"uuid": "c1"}]


async def test_get_shopping_cart_empty(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api._cart_get_items.asyncio",
        new=AsyncMock(return_value=None),
    ):
        assert await api.get_shopping_cart(LIST_ID) == []


async def test_lookup_barcode(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api.barcode_controller_find_one.asyncio",
        new=AsyncMock(return_value=_make_dto(name="Bananas")),
    ):
        result = await api.lookup_barcode("123")
    assert result == {"name": "Bananas"}


async def test_lookup_barcode_unknown(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api.barcode_controller_find_one.asyncio",
        new=AsyncMock(return_value=None),
    ):
        assert await api.lookup_barcode("xx") is None
