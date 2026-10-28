from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.auto_reduce_cursor_dto import AutoReduceCursorDto
from ...types import Response


def _get_kwargs(
    list_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/list/{list_id}/auto-reduce/cursor".format(
            list_id=quote(str(list_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | AutoReduceCursorDto:
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    response_default = AutoReduceCursorDto.from_dict(response.json())

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | AutoReduceCursorDto]:
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
) -> Response[Any | AutoReduceCursorDto]:
    """Get the list-wide auto-reduce cursor

     Start of the next accrual window, shared by every member of the list. Null until the modal has been
    presented for this list once; the app then falls back to its per-user baseline.

    Args:
        list_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AutoReduceCursorDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    *,
    client: AuthenticatedClient,
) -> Any | AutoReduceCursorDto | None:
    """Get the list-wide auto-reduce cursor

     Start of the next accrual window, shared by every member of the list. Null until the modal has been
    presented for this list once; the app then falls back to its per-user baseline.

    Args:
        list_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AutoReduceCursorDto
    """

    return sync_detailed(
        list_id=list_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | AutoReduceCursorDto]:
    """Get the list-wide auto-reduce cursor

     Start of the next accrual window, shared by every member of the list. Null until the modal has been
    presented for this list once; the app then falls back to its per-user baseline.

    Args:
        list_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AutoReduceCursorDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    *,
    client: AuthenticatedClient,
) -> Any | AutoReduceCursorDto | None:
    """Get the list-wide auto-reduce cursor

     Start of the next accrual window, shared by every member of the list. Null until the modal has been
    presented for this list once; the app then falls back to its per-user baseline.

    Args:
        list_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AutoReduceCursorDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            client=client,
        )
    ).parsed
