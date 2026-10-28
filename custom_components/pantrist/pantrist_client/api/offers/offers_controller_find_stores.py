from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.store_dto import StoreDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    lat: float | Unset = UNSET,
    lng: float | Unset = UNSET,
    zip_: str | Unset = UNSET,
    radius: float | Unset = 10000.0,
    retailer_key: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["lat"] = lat

    params["lng"] = lng

    params["zip"] = zip_

    params["radius"] = radius

    params["retailerKey"] = retailer_key

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/offers/stores",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> list[StoreDto] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = StoreDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[list[StoreDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    lat: float | Unset = UNSET,
    lng: float | Unset = UNSET,
    zip_: str | Unset = UNSET,
    radius: float | Unset = 10000.0,
    retailer_key: str | Unset = UNSET,
) -> Response[list[StoreDto]]:
    """Find markets near a coordinate or inside a postal code

     Pass lat/lng (coarse accuracy is enough) or zip. The postal-code path exists because a large share
    of users decline the location permission.

    Args:
        lat (float | Unset):
        lng (float | Unset):
        zip_ (str | Unset):
        radius (float | Unset):  Default: 10000.0.
        retailer_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[StoreDto]]
    """

    kwargs = _get_kwargs(
        lat=lat,
        lng=lng,
        zip_=zip_,
        radius=radius,
        retailer_key=retailer_key,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    lat: float | Unset = UNSET,
    lng: float | Unset = UNSET,
    zip_: str | Unset = UNSET,
    radius: float | Unset = 10000.0,
    retailer_key: str | Unset = UNSET,
) -> list[StoreDto] | None:
    """Find markets near a coordinate or inside a postal code

     Pass lat/lng (coarse accuracy is enough) or zip. The postal-code path exists because a large share
    of users decline the location permission.

    Args:
        lat (float | Unset):
        lng (float | Unset):
        zip_ (str | Unset):
        radius (float | Unset):  Default: 10000.0.
        retailer_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[StoreDto]
    """

    return sync_detailed(
        client=client,
        lat=lat,
        lng=lng,
        zip_=zip_,
        radius=radius,
        retailer_key=retailer_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    lat: float | Unset = UNSET,
    lng: float | Unset = UNSET,
    zip_: str | Unset = UNSET,
    radius: float | Unset = 10000.0,
    retailer_key: str | Unset = UNSET,
) -> Response[list[StoreDto]]:
    """Find markets near a coordinate or inside a postal code

     Pass lat/lng (coarse accuracy is enough) or zip. The postal-code path exists because a large share
    of users decline the location permission.

    Args:
        lat (float | Unset):
        lng (float | Unset):
        zip_ (str | Unset):
        radius (float | Unset):  Default: 10000.0.
        retailer_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[StoreDto]]
    """

    kwargs = _get_kwargs(
        lat=lat,
        lng=lng,
        zip_=zip_,
        radius=radius,
        retailer_key=retailer_key,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    lat: float | Unset = UNSET,
    lng: float | Unset = UNSET,
    zip_: str | Unset = UNSET,
    radius: float | Unset = 10000.0,
    retailer_key: str | Unset = UNSET,
) -> list[StoreDto] | None:
    """Find markets near a coordinate or inside a postal code

     Pass lat/lng (coarse accuracy is enough) or zip. The postal-code path exists because a large share
    of users decline the location permission.

    Args:
        lat (float | Unset):
        lng (float | Unset):
        zip_ (str | Unset):
        radius (float | Unset):  Default: 10000.0.
        retailer_key (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[StoreDto]
    """

    return (
        await asyncio_detailed(
            client=client,
            lat=lat,
            lng=lng,
            zip_=zip_,
            radius=radius,
            retailer_key=retailer_key,
        )
    ).parsed
