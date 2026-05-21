from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...models.barcode_page_dto import BarcodePageDto
from ...types import Response


def _get_kwargs(
    barcode: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/barcodes/{barcode}/page".format(
            barcode=quote(str(barcode), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> BarcodePageDto:
    response_default = BarcodePageDto.from_dict(response.json())

    return response_default


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[BarcodePageDto]:
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
) -> Response[BarcodePageDto]:
    """Full SSR payload for a barcode detail page (name, image, offers, related, indexable). Localized copy
    is built client-side.

    Args:
        barcode (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BarcodePageDto]
    """

    kwargs = _get_kwargs(
        barcode=barcode,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    barcode: str,
    *,
    client: AuthenticatedClient | Client,
) -> BarcodePageDto | None:
    """Full SSR payload for a barcode detail page (name, image, offers, related, indexable). Localized copy
    is built client-side.

    Args:
        barcode (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BarcodePageDto
    """

    return sync_detailed(
        barcode=barcode,
        client=client,
    ).parsed


async def asyncio_detailed(
    barcode: str,
    *,
    client: AuthenticatedClient | Client,
) -> Response[BarcodePageDto]:
    """Full SSR payload for a barcode detail page (name, image, offers, related, indexable). Localized copy
    is built client-side.

    Args:
        barcode (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BarcodePageDto]
    """

    kwargs = _get_kwargs(
        barcode=barcode,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    barcode: str,
    *,
    client: AuthenticatedClient | Client,
) -> BarcodePageDto | None:
    """Full SSR payload for a barcode detail page (name, image, offers, related, indexable). Localized copy
    is built client-side.

    Args:
        barcode (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BarcodePageDto
    """

    return (
        await asyncio_detailed(
            barcode=barcode,
            client=client,
        )
    ).parsed
