from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.price_trend_detail_dto import PriceTrendDetailDto
from ...types import Response


def _get_kwargs(
    list_id: str,
    product_key: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/list/{list_id}/price-trends/{product_key}".format(
            list_id=quote(str(list_id), safe=""),
            product_key=quote(str(product_key), safe=""),
        ),
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | PriceTrendDetailDto | None:
    if response.status_code == 200:
        response_200 = PriceTrendDetailDto.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | PriceTrendDetailDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    list_id: str,
    product_key: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | PriceTrendDetailDto]:
    """Full purchase history + detected content changes for one product.

    Args:
        list_id (str):
        product_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PriceTrendDetailDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        product_key=product_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    product_key: str,
    *,
    client: AuthenticatedClient,
) -> Any | PriceTrendDetailDto | None:
    """Full purchase history + detected content changes for one product.

    Args:
        list_id (str):
        product_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PriceTrendDetailDto
    """

    return sync_detailed(
        list_id=list_id,
        product_key=product_key,
        client=client,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    product_key: str,
    *,
    client: AuthenticatedClient,
) -> Response[Any | PriceTrendDetailDto]:
    """Full purchase history + detected content changes for one product.

    Args:
        list_id (str):
        product_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PriceTrendDetailDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        product_key=product_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    product_key: str,
    *,
    client: AuthenticatedClient,
) -> Any | PriceTrendDetailDto | None:
    """Full purchase history + detected content changes for one product.

    Args:
        list_id (str):
        product_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PriceTrendDetailDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            product_key=product_key,
            client=client,
        )
    ).parsed
