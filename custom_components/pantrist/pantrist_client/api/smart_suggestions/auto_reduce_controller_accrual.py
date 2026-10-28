from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...types import UNSET, Response


def _get_kwargs(
    list_id: str,
    *,
    since: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["since"] = since

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/list/{list_id}/auto-reduce/accrual".format(
            list_id=quote(str(list_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | None:
    if response.status_code == 200:
        return None

    if response.status_code == 403:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any]:
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
    since: str,
) -> Response[Any]:
    """Get suggested deltas since the cursor

     `since` is the caller's baseline. Each item resolves its own window from the point it was last
    accounted for, so members of a shared list are not asked for a window another member already
    confirmed. A non-empty result marks exactly the returned items as accounted for as of NOW: the app
    presents the modal precisely when rows come back, so those items count as seen from here on. Items
    that are NOT returned keep the consumption they have accrued, which is what the list-wide cursor
    bump used to destroy.

    Args:
        list_id (str):
        since (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        since=since,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    list_id: str,
    *,
    client: AuthenticatedClient,
    since: str,
) -> Response[Any]:
    """Get suggested deltas since the cursor

     `since` is the caller's baseline. Each item resolves its own window from the point it was last
    accounted for, so members of a shared list are not asked for a window another member already
    confirmed. A non-empty result marks exactly the returned items as accounted for as of NOW: the app
    presents the modal precisely when rows come back, so those items count as seen from here on. Items
    that are NOT returned keep the consumption they have accrued, which is what the list-wide cursor
    bump used to destroy.

    Args:
        list_id (str):
        since (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        since=since,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
