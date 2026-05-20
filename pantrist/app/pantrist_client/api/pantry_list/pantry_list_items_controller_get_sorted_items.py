from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.article_dto import ArticleDto
from ...models.pantry_list_items_controller_get_sorted_items_order import PantryListItemsControllerGetSortedItemsOrder
from ...models.pantry_list_items_controller_get_sorted_items_sort_by import (
    PantryListItemsControllerGetSortedItemsSortBy,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    *,
    sort_by: PantryListItemsControllerGetSortedItemsSortBy,
    order: PantryListItemsControllerGetSortedItemsOrder | Unset = UNSET,
    limit: float | Unset = UNSET,
    start_after_timestamp: float | Unset = UNSET,
    start_after_best_before: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_sort_by = sort_by.value
    params["sortBy"] = json_sort_by

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order.value

    params["order"] = json_order

    params["limit"] = limit

    params["startAfterTimestamp"] = start_after_timestamp

    params["startAfterBestBefore"] = start_after_best_before

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/list/{list_id}/pantryList/sorted".format(
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
    sort_by: PantryListItemsControllerGetSortedItemsSortBy,
    order: PantryListItemsControllerGetSortedItemsOrder | Unset = UNSET,
    limit: float | Unset = UNSET,
    start_after_timestamp: float | Unset = UNSET,
    start_after_best_before: str | Unset = UNSET,
) -> Response[list[ArticleDto]]:
    """Get pantry list items sorted and paginated

    Args:
        list_id (str):
        sort_by (PantryListItemsControllerGetSortedItemsSortBy):
        order (PantryListItemsControllerGetSortedItemsOrder | Unset):
        limit (float | Unset):
        start_after_timestamp (float | Unset):
        start_after_best_before (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[ArticleDto]]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        sort_by=sort_by,
        order=order,
        limit=limit,
        start_after_timestamp=start_after_timestamp,
        start_after_best_before=start_after_best_before,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    *,
    client: AuthenticatedClient,
    sort_by: PantryListItemsControllerGetSortedItemsSortBy,
    order: PantryListItemsControllerGetSortedItemsOrder | Unset = UNSET,
    limit: float | Unset = UNSET,
    start_after_timestamp: float | Unset = UNSET,
    start_after_best_before: str | Unset = UNSET,
) -> list[ArticleDto] | None:
    """Get pantry list items sorted and paginated

    Args:
        list_id (str):
        sort_by (PantryListItemsControllerGetSortedItemsSortBy):
        order (PantryListItemsControllerGetSortedItemsOrder | Unset):
        limit (float | Unset):
        start_after_timestamp (float | Unset):
        start_after_best_before (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[ArticleDto]
    """

    return sync_detailed(
        list_id=list_id,
        client=client,
        sort_by=sort_by,
        order=order,
        limit=limit,
        start_after_timestamp=start_after_timestamp,
        start_after_best_before=start_after_best_before,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    *,
    client: AuthenticatedClient,
    sort_by: PantryListItemsControllerGetSortedItemsSortBy,
    order: PantryListItemsControllerGetSortedItemsOrder | Unset = UNSET,
    limit: float | Unset = UNSET,
    start_after_timestamp: float | Unset = UNSET,
    start_after_best_before: str | Unset = UNSET,
) -> Response[list[ArticleDto]]:
    """Get pantry list items sorted and paginated

    Args:
        list_id (str):
        sort_by (PantryListItemsControllerGetSortedItemsSortBy):
        order (PantryListItemsControllerGetSortedItemsOrder | Unset):
        limit (float | Unset):
        start_after_timestamp (float | Unset):
        start_after_best_before (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[ArticleDto]]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        sort_by=sort_by,
        order=order,
        limit=limit,
        start_after_timestamp=start_after_timestamp,
        start_after_best_before=start_after_best_before,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    *,
    client: AuthenticatedClient,
    sort_by: PantryListItemsControllerGetSortedItemsSortBy,
    order: PantryListItemsControllerGetSortedItemsOrder | Unset = UNSET,
    limit: float | Unset = UNSET,
    start_after_timestamp: float | Unset = UNSET,
    start_after_best_before: str | Unset = UNSET,
) -> list[ArticleDto] | None:
    """Get pantry list items sorted and paginated

    Args:
        list_id (str):
        sort_by (PantryListItemsControllerGetSortedItemsSortBy):
        order (PantryListItemsControllerGetSortedItemsOrder | Unset):
        limit (float | Unset):
        start_after_timestamp (float | Unset):
        start_after_best_before (str | Unset):

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
            sort_by=sort_by,
            order=order,
            limit=limit,
            start_after_timestamp=start_after_timestamp,
            start_after_best_before=start_after_best_before,
        )
    ).parsed
