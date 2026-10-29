"""PantristApi wrapper tests."""

from __future__ import annotations

from collections.abc import AsyncGenerator
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
async def api() -> AsyncGenerator[PantristApi, None]:
    """An API wrapper with a stubbed OAuth2 session — no real HA needed."""
    hass = MagicMock()
    # Run executor jobs inline so the lazily-built SSL context (used when the
    # shared httpx client is constructed) resolves without a real HA loop.
    async def _run_executor_job(func: Any, *args: Any) -> Any:
        return func(*args)

    hass.async_add_executor_job = AsyncMock(side_effect=_run_executor_job)
    session = MagicMock()
    session.async_ensure_token_valid = AsyncMock()
    session.token = {"access_token": "tok"}
    wrapper = PantristApi(hass, session)
    yield wrapper
    # Close the shared httpx client built lazily by ``_client()``.
    await wrapper.async_close()


async def test_client_refreshes_token(api: PantristApi) -> None:
    client = await api._client()
    session: Any = api._session
    session.async_ensure_token_valid.assert_awaited_once()
    assert client.token == "tok"


async def test_client_injects_shared_httpx_client(api: PantristApi) -> None:
    """The AuthenticatedClient uses our pre-built, auth-stamped httpx client."""
    client = await api._client()
    httpx_client = client.get_async_httpx_client()
    # No new client is constructed inside the loop — the injected one is used.
    assert httpx_client is api._httpx_client
    assert httpx_client.headers["Authorization"] == "Bearer tok"


async def test_ssl_context_built_in_executor(api: PantristApi) -> None:
    """The SSL context is built off-loop so no blocking call hits the loop."""
    from custom_components.pantrist import api as api_module

    await api._client()
    hass: Any = api._hass
    hass.async_add_executor_job.assert_awaited_once_with(api_module.client_context)


async def test_httpx_client_reused_across_calls(api: PantristApi) -> None:
    """The shared httpx client (and its SSL context) is built exactly once."""
    await api._client()
    await api._client()
    hass: Any = api._hass
    assert hass.async_add_executor_job.await_count == 1


async def test_async_close_disposes_httpx_client(api: PantristApi) -> None:
    await api._client()
    assert api._httpx_client is not None
    await api.async_close()
    assert api._httpx_client is None
    # Idempotent — closing again with nothing open is a no-op.
    await api.async_close()


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
    """An account with no lists answers with an empty list, and that is fine."""
    with patch(
        "custom_components.pantrist.api.list_controller_get_list.asyncio",
        new=AsyncMock(return_value=[]),
    ):
        assert await api.get_lists() == []


async def test_get_lists_raises_when_the_endpoint_did_not_answer(
    api: PantristApi,
) -> None:
    """``None`` means a non-2xx the generated client swallowed, not "no lists".

    Returning ``[]`` here let a 401 or a 502 look like the user having
    deleted everything, and the reconcile loop removed every device.
    """
    with patch(
        "custom_components.pantrist.api.list_controller_get_list.asyncio",
        new=AsyncMock(return_value=None),
    ):
        with pytest.raises(PantristApiError):
            await api.get_lists()


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


# A pantry item as the API returns it, open package and best-before included.
_ARTICLE = {
    "uuid": "b3e36141-4031-4681-95b1-5c0bd9a68895",
    "name": "Basmatireis",
    "brand": None,
    "categoryUuid": "23",
    "amount": 1,
    "contentVolume": 1,
    "unitId": "pieces",
    "manageMinimumAmount": False,
    "minimumAmount": 1,
    "minimumAmountMode": "packages",
    "amountToBuy": 1,
    "priceType": "perUnit",
    "discountType": "currency",
    "discountPerUnitOrTotal": "total",
    "notes": "Vorratsschrank oben",
    "lastModified": 1793191110828,
    "pantrySettings": {
        "articleList": [
            {"pantryUuid": "1", "count": 1, "bestBefore": "2027-03-01",
             "articleIsOpen": True, "remainingAmount": 40}
        ],
        "earliestBestBefore": "2027-03-01",
    },
}


def _patched(article):
    """Patch the get/put/change endpoints around a real ArticleDto."""
    from contextlib import ExitStack

    stack = ExitStack()
    stack.enter_context(patch(
        "custom_components.pantrist.api._pantry_get_item.asyncio",
        new=AsyncMock(return_value=article),
    ))
    upsert = stack.enter_context(patch(
        "custom_components.pantrist.api._pantry_upsert_item.asyncio",
        new=AsyncMock(side_effect=lambda **kw: kw["body"]),
    ))
    return stack, upsert


async def test_update_pantry_item_keeps_the_rest(api: PantristApi) -> None:
    """Only the given fields change; everything else goes back as it came."""
    from custom_components.pantrist.pantrist_client.models import ArticleDto

    article = ArticleDto.from_dict(_ARTICLE)
    before = article.to_dict()
    stack, upsert = _patched(article)
    with stack:
        result = await api.update_pantry_item(
            LIST_ID,
            _ARTICLE["uuid"],
            {"contentVolume": 500, "unitId": "g", "minimumAmount": 2},
        )
    kwargs = upsert.await_args.kwargs
    assert kwargs["list_id"] == LIST_ID
    assert kwargs["item_id"] == _ARTICLE["uuid"]
    # Setting a minimum switches tracking on, as in the app.
    assert kwargs["body"].to_dict() == {
        **before,
        "contentVolume": 500,
        "unitId": "g",
        "minimumAmount": 2,
        "manageMinimumAmount": True,
    }
    assert result["contentVolume"] == 500


async def test_update_pantry_item_amount_goes_through_the_delta(
    api: PantristApi,
) -> None:
    """A new amount is sent as a change, so the stock batches stay right."""
    from custom_components.pantrist.pantrist_client.models import ArticleDto

    stack, upsert = _patched(ArticleDto.from_dict({**_ARTICLE, "amount": 1}))
    with stack, patch.object(
        api, "change_pantry_item_amount", new=AsyncMock(return_value={"amount": 4})
    ) as change:
        result = await api.update_pantry_item(LIST_ID, _ARTICLE["uuid"], {}, amount=4)
    upsert.assert_not_awaited()
    change.assert_awaited_once_with(LIST_ID, _ARTICLE["uuid"], change=3)
    assert result == {"amount": 4}


async def test_update_pantry_item_unchanged_amount_sends_nothing(
    api: PantristApi,
) -> None:
    from custom_components.pantrist.pantrist_client.models import ArticleDto

    stack, upsert = _patched(ArticleDto.from_dict(_ARTICLE))
    with stack, patch.object(api, "change_pantry_item_amount", new=AsyncMock()) as change:
        await api.update_pantry_item(LIST_ID, _ARTICLE["uuid"], {}, amount=1)
    upsert.assert_not_awaited()
    change.assert_not_awaited()


async def test_update_pantry_item_missing_item(api: PantristApi) -> None:
    with patch(
        "custom_components.pantrist.api._pantry_get_item.asyncio",
        new=AsyncMock(return_value=None),
    ), pytest.raises(PantristApiError):
        await api.update_pantry_item(LIST_ID, "gone", {"name": "x"})


def test_apply_changes_best_before_goes_to_every_batch() -> None:
    from custom_components.pantrist.api import apply_pantry_item_changes

    current = {
        "amount": 3,
        "pantrySettings": {
            "articleList": [
                {"pantryUuid": "1", "count": 2, "bestBefore": "2026-01-01",
                 "calculatedBestBeforeDate": True},
                {"pantryUuid": "2", "count": 1},
            ],
            "earliestBestBefore": "2026-01-01",
        },
    }
    merged = apply_pantry_item_changes(current, {"bestBefore": "2026-12-24"})
    assert merged["pantrySettings"] == {
        "articleList": [
            {"pantryUuid": "1", "count": 2, "bestBefore": "2026-12-24",
             "calculatedBestBeforeDate": False},
            {"pantryUuid": "2", "count": 1, "bestBefore": "2026-12-24",
             "calculatedBestBeforeDate": False},
        ],
        "earliestBestBefore": "2026-12-24",
    }
    # The input is left alone.
    assert current["pantrySettings"]["earliestBestBefore"] == "2026-01-01"


def test_apply_changes_clears_and_creates_a_batch() -> None:
    from custom_components.pantrist.api import apply_pantry_item_changes

    dated = {"amount": 1, "brand": "Acme", "pantrySettings": {
        "articleList": [{"pantryUuid": "1", "count": 1, "bestBefore": "2026-01-01"}],
        "earliestBestBefore": "2026-01-01",
    }}
    cleared = apply_pantry_item_changes(dated, {"bestBefore": None, "brand": None})
    assert cleared["brand"] is None
    assert cleared["pantrySettings"] == {
        "articleList": [{"pantryUuid": "1", "count": 1}]
    }
    # No batch yet: the date lands on one in the default pantry.
    undated = {"amount": 2, "pantrySettings": {"articleList": []}}
    merged = apply_pantry_item_changes(undated, {"bestBefore": "2027-01-01"})
    assert merged["pantrySettings"]["articleList"] == [
        {"pantryUuid": "1", "count": 2, "bestBefore": "2027-01-01",
         "calculatedBestBeforeDate": False}
    ]


def test_apply_changes_tracking_off_keeps_the_minimum() -> None:
    from custom_components.pantrist.api import apply_pantry_item_changes

    current = {"minimumAmount": 2, "manageMinimumAmount": True}
    merged = apply_pantry_item_changes(current, {"manageMinimumAmount": False})
    assert merged == {"minimumAmount": 2, "manageMinimumAmount": False}
    # An explicit "off" wins over the implied "on".
    merged = apply_pantry_item_changes(
        current, {"minimumAmount": 3, "manageMinimumAmount": False}
    )
    assert merged == {"minimumAmount": 3, "manageMinimumAmount": False}
