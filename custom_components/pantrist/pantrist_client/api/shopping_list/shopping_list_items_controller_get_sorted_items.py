from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.article_dto import ArticleDto
from ...models.shopping_list_items_controller_get_sorted_items_order import (
    ShoppingListItemsControllerGetSortedItemsOrder,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    *,
    order: ShoppingListItemsControllerGetSortedItemsOrder | Unset = UNSET,
    limit: float | Unset = UNSET,
    start_after_timestamp: float | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["limit"] = limit

    params["startAfterTimestamp"] = start_after_timestamp

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/list/{list_id}/shoppingList/sorted".format(
            list_id=quote(str(list_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> list[ArticleDto] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ArticleDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[list[ArticleDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    list_id: str,
    *,
    client: AuthenticatedClient,
    order: ShoppingListItemsControllerGetSortedItemsOrder | Unset = UNSET,
    limit: float | Unset = UNSET,
    start_after_timestamp: float | Unset = UNSET,
) -> Response[list[ArticleDto]]:
    """Get shopping list items sorted by timestamp and paginated

    Args:
        list_id (str):
        order (ShoppingListItemsControllerGetSortedItemsOrder | Unset):
        limit (float | Unset):
        start_after_timestamp (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[ArticleDto]]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        order=order,
        limit=limit,
        start_after_timestamp=start_after_timestamp,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    *,
    client: AuthenticatedClient,
    order: ShoppingListItemsControllerGetSortedItemsOrder | Unset = UNSET,
    limit: float | Unset = UNSET,
    start_after_timestamp: float | Unset = UNSET,
) -> list[ArticleDto] | None:
    """Get shopping list items sorted by timestamp and paginated

    Args:
        list_id (str):
        order (ShoppingListItemsControllerGetSortedItemsOrder | Unset):
        limit (float | Unset):
        start_after_timestamp (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[ArticleDto]
    """

    return sync_detailed(
        list_id=list_id,
        client=client,
        order=order,
        limit=limit,
        start_after_timestamp=start_after_timestamp,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    *,
    client: AuthenticatedClient,
    order: ShoppingListItemsControllerGetSortedItemsOrder | Unset = UNSET,
    limit: float | Unset = UNSET,
    start_after_timestamp: float | Unset = UNSET,
) -> Response[list[ArticleDto]]:
    """Get shopping list items sorted by timestamp and paginated

    Args:
        list_id (str):
        order (ShoppingListItemsControllerGetSortedItemsOrder | Unset):
        limit (float | Unset):
        start_after_timestamp (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[ArticleDto]]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        order=order,
        limit=limit,
        start_after_timestamp=start_after_timestamp,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    *,
    client: AuthenticatedClient,
    order: ShoppingListItemsControllerGetSortedItemsOrder | Unset = UNSET,
    limit: float | Unset = UNSET,
    start_after_timestamp: float | Unset = UNSET,
) -> list[ArticleDto] | None:
    """Get shopping list items sorted by timestamp and paginated

    Args:
        list_id (str):
        order (ShoppingListItemsControllerGetSortedItemsOrder | Unset):
        limit (float | Unset):
        start_after_timestamp (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[ArticleDto]
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            client=client,
            order=order,
            limit=limit,
            start_after_timestamp=start_after_timestamp,
        )
    ).parsed
