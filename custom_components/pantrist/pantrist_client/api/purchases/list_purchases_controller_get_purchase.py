from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.purchased_item_dto import PurchasedItemDto
from ...types import Response


def _get_kwargs(
    list_id: str,
    purchase_row_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/list/{list_id}/purchases/{purchase_row_id}".format(
            list_id=quote(str(list_id), safe=""),
            purchase_row_id=quote(str(purchase_row_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PurchasedItemDto | None:
    if response.status_code == 200:
        response_200 = PurchasedItemDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PurchasedItemDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    list_id: str,
    purchase_row_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[PurchasedItemDto]:
    """Get a single purchase by its row ID

    Args:
        list_id (str):
        purchase_row_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PurchasedItemDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        purchase_row_id=purchase_row_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    purchase_row_id: str,
    *,
    client: AuthenticatedClient,
) -> PurchasedItemDto | None:
    """Get a single purchase by its row ID

    Args:
        list_id (str):
        purchase_row_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PurchasedItemDto
    """

    return sync_detailed(
        list_id=list_id,
        purchase_row_id=purchase_row_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    purchase_row_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[PurchasedItemDto]:
    """Get a single purchase by its row ID

    Args:
        list_id (str):
        purchase_row_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PurchasedItemDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        purchase_row_id=purchase_row_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    purchase_row_id: str,
    *,
    client: AuthenticatedClient,
) -> PurchasedItemDto | None:
    """Get a single purchase by its row ID

    Args:
        list_id (str):
        purchase_row_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PurchasedItemDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            purchase_row_id=purchase_row_id,
            client=client,
        )
    ).parsed
