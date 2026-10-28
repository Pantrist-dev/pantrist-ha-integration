from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.price_trends_page_dto import PriceTrendsPageDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    *,
    market: str | Unset = UNSET,
    since: str | Unset = UNSET,
    limit: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    search: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["market"] = market

    params["since"] = since

    params["limit"] = limit

    params["cursor"] = cursor

    params["search"] = search

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/list/{list_id}/price-trends".format(
            list_id=quote(str(list_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PriceTrendsPageDto | None:
    if response.status_code == 200:
        response_200 = PriceTrendsPageDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PriceTrendsPageDto]:
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
    market: str | Unset = UNSET,
    since: str | Unset = UNSET,
    limit: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    search: str | Unset = UNSET,
) -> Response[PriceTrendsPageDto]:
    """Aggregated price history per product. Groups purchases by barcode (preferred) or normalized
    name+brand.

    Args:
        list_id (str):
        market (str | Unset):
        since (str | Unset):
        limit (float | Unset):
        cursor (str | Unset):
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PriceTrendsPageDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        market=market,
        since=since,
        limit=limit,
        cursor=cursor,
        search=search,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    *,
    client: AuthenticatedClient,
    market: str | Unset = UNSET,
    since: str | Unset = UNSET,
    limit: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    search: str | Unset = UNSET,
) -> PriceTrendsPageDto | None:
    """Aggregated price history per product. Groups purchases by barcode (preferred) or normalized
    name+brand.

    Args:
        list_id (str):
        market (str | Unset):
        since (str | Unset):
        limit (float | Unset):
        cursor (str | Unset):
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PriceTrendsPageDto
    """

    return sync_detailed(
        list_id=list_id,
        client=client,
        market=market,
        since=since,
        limit=limit,
        cursor=cursor,
        search=search,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    *,
    client: AuthenticatedClient,
    market: str | Unset = UNSET,
    since: str | Unset = UNSET,
    limit: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    search: str | Unset = UNSET,
) -> Response[PriceTrendsPageDto]:
    """Aggregated price history per product. Groups purchases by barcode (preferred) or normalized
    name+brand.

    Args:
        list_id (str):
        market (str | Unset):
        since (str | Unset):
        limit (float | Unset):
        cursor (str | Unset):
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PriceTrendsPageDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        market=market,
        since=since,
        limit=limit,
        cursor=cursor,
        search=search,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    *,
    client: AuthenticatedClient,
    market: str | Unset = UNSET,
    since: str | Unset = UNSET,
    limit: float | Unset = UNSET,
    cursor: str | Unset = UNSET,
    search: str | Unset = UNSET,
) -> PriceTrendsPageDto | None:
    """Aggregated price history per product. Groups purchases by barcode (preferred) or normalized
    name+brand.

    Args:
        list_id (str):
        market (str | Unset):
        since (str | Unset):
        limit (float | Unset):
        cursor (str | Unset):
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PriceTrendsPageDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            client=client,
            market=market,
            since=since,
            limit=limit,
            cursor=cursor,
            search=search,
        )
    ).parsed
