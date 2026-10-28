from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.purchase_page_dto import PurchasePageDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    *,
    before: str | Unset = UNSET,
    limit: float | Unset = UNSET,
    until: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["before"] = before

    params["limit"] = limit

    params["until"] = until

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/list/{list_id}/purchases/recent".format(
            list_id=quote(str(list_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PurchasePageDto | None:
    if response.status_code == 200:
        response_200 = PurchasePageDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PurchasePageDto]:
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
    before: str | Unset = UNSET,
    limit: float | Unset = UNSET,
    until: str | Unset = UNSET,
) -> Response[PurchasePageDto]:
    """Purchase history, newest first, paged. Follow `nextCursor` via `before` until it is absent.

    Args:
        list_id (str):
        before (str | Unset):
        limit (float | Unset):
        until (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PurchasePageDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        before=before,
        limit=limit,
        until=until,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    *,
    client: AuthenticatedClient,
    before: str | Unset = UNSET,
    limit: float | Unset = UNSET,
    until: str | Unset = UNSET,
) -> PurchasePageDto | None:
    """Purchase history, newest first, paged. Follow `nextCursor` via `before` until it is absent.

    Args:
        list_id (str):
        before (str | Unset):
        limit (float | Unset):
        until (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PurchasePageDto
    """

    return sync_detailed(
        list_id=list_id,
        client=client,
        before=before,
        limit=limit,
        until=until,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    *,
    client: AuthenticatedClient,
    before: str | Unset = UNSET,
    limit: float | Unset = UNSET,
    until: str | Unset = UNSET,
) -> Response[PurchasePageDto]:
    """Purchase history, newest first, paged. Follow `nextCursor` via `before` until it is absent.

    Args:
        list_id (str):
        before (str | Unset):
        limit (float | Unset):
        until (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PurchasePageDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        before=before,
        limit=limit,
        until=until,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    *,
    client: AuthenticatedClient,
    before: str | Unset = UNSET,
    limit: float | Unset = UNSET,
    until: str | Unset = UNSET,
) -> PurchasePageDto | None:
    """Purchase history, newest first, paged. Follow `nextCursor` via `before` until it is absent.

    Args:
        list_id (str):
        before (str | Unset):
        limit (float | Unset):
        until (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PurchasePageDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            client=client,
            before=before,
            limit=limit,
            until=until,
        )
    ).parsed
