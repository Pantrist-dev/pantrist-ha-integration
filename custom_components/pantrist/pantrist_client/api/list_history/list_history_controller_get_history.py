from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_item_history_page_dto import ListItemHistoryPageDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    *,
    limit: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/list/{list_id}/history".format(
            list_id=quote(str(list_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ListItemHistoryPageDto | None:
    if response.status_code == 200:
        response_200 = ListItemHistoryPageDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ListItemHistoryPageDto]:
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
    limit: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[ListItemHistoryPageDto]:
    """Paginated change history for every item in a list, newest first.

    Args:
        list_id (str):
        limit (float | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListItemHistoryPageDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        limit=limit,
        cursor=cursor,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    *,
    client: AuthenticatedClient,
    limit: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> ListItemHistoryPageDto | None:
    """Paginated change history for every item in a list, newest first.

    Args:
        list_id (str):
        limit (float | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListItemHistoryPageDto
    """

    return sync_detailed(
        list_id=list_id,
        client=client,
        limit=limit,
        cursor=cursor,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    *,
    client: AuthenticatedClient,
    limit: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> Response[ListItemHistoryPageDto]:
    """Paginated change history for every item in a list, newest first.

    Args:
        list_id (str):
        limit (float | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListItemHistoryPageDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        limit=limit,
        cursor=cursor,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    *,
    client: AuthenticatedClient,
    limit: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
) -> ListItemHistoryPageDto | None:
    """Paginated change history for every item in a list, newest first.

    Args:
        list_id (str):
        limit (float | Unset):
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListItemHistoryPageDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            client=client,
            limit=limit,
            cursor=cursor,
        )
    ).parsed
