from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_item_history_dto import ListItemHistoryDto
from ...types import Response


def _get_kwargs(
    list_id: str,
    history_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/list/{list_id}/history/{history_id}/revert".format(
            list_id=quote(str(list_id), safe=""),
            history_id=quote(str(history_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ListItemHistoryDto | None:
    if response.status_code == 200:
        response_200 = ListItemHistoryDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ListItemHistoryDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    list_id: str,
    history_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ListItemHistoryDto]:
    """Revert a single history entry. Always wins over later edits; the revert itself is recorded as a new
    entry. The resulting item event is broadcast to every client in the list, including the user that
    triggered the revert.

    Args:
        list_id (str):
        history_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListItemHistoryDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        history_id=history_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    history_id: str,
    *,
    client: AuthenticatedClient,
) -> ListItemHistoryDto | None:
    """Revert a single history entry. Always wins over later edits; the revert itself is recorded as a new
    entry. The resulting item event is broadcast to every client in the list, including the user that
    triggered the revert.

    Args:
        list_id (str):
        history_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListItemHistoryDto
    """

    return sync_detailed(
        list_id=list_id,
        history_id=history_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    history_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[ListItemHistoryDto]:
    """Revert a single history entry. Always wins over later edits; the revert itself is recorded as a new
    entry. The resulting item event is broadcast to every client in the list, including the user that
    triggered the revert.

    Args:
        list_id (str):
        history_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListItemHistoryDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        history_id=history_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    history_id: str,
    *,
    client: AuthenticatedClient,
) -> ListItemHistoryDto | None:
    """Revert a single history entry. Always wins over later edits; the revert itself is recorded as a new
    entry. The resulting item event is broadcast to every client in the list, including the user that
    triggered the revert.

    Args:
        list_id (str):
        history_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListItemHistoryDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            history_id=history_id,
            client=client,
        )
    ).parsed
