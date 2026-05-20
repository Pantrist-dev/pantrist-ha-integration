from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.affiliate_product_dto import AffiliateProductDto
from ...types import Response


def _get_kwargs(
    barcode: str,
    *,
    pantrist_market: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["pantrist-market"] = pantrist_market

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/affiliate/{barcode}".format(
            barcode=quote(str(barcode), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> list[AffiliateProductDto]:
    response_default = []
    _response_default = response.json()
    for response_default_item_data in _response_default:
        response_default_item = AffiliateProductDto.from_dict(response_default_item_data)

        response_default.append(response_default_item)

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[AffiliateProductDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    barcode: str,
    *,
    client: AuthenticatedClient | Client,
    pantrist_market: str,
) -> Response[list[AffiliateProductDto]]:
    """
    Args:
        barcode (str):
        pantrist_market (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[AffiliateProductDto]]
    """

    kwargs = _get_kwargs(
        barcode=barcode,
        pantrist_market=pantrist_market,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    barcode: str,
    *,
    client: AuthenticatedClient | Client,
    pantrist_market: str,
) -> list[AffiliateProductDto] | None:
    """
    Args:
        barcode (str):
        pantrist_market (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[AffiliateProductDto]
    """

    return sync_detailed(
        barcode=barcode,
        client=client,
        pantrist_market=pantrist_market,
    ).parsed


async def asyncio_detailed(
    barcode: str,
    *,
    client: AuthenticatedClient | Client,
    pantrist_market: str,
) -> Response[list[AffiliateProductDto]]:
    """
    Args:
        barcode (str):
        pantrist_market (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[AffiliateProductDto]]
    """

    kwargs = _get_kwargs(
        barcode=barcode,
        pantrist_market=pantrist_market,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    barcode: str,
    *,
    client: AuthenticatedClient | Client,
    pantrist_market: str,
) -> list[AffiliateProductDto] | None:
    """
    Args:
        barcode (str):
        pantrist_market (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[AffiliateProductDto]
    """

    return (
        await asyncio_detailed(
            barcode=barcode,
            client=client,
            pantrist_market=pantrist_market,
        )
    ).parsed
