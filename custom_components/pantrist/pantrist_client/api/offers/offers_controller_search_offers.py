from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offer_search_result_dto import OfferSearchResultDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: str,
    lat: float,
    lng: float,
    radius: float | Unset = 10000.0,
    language: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["q"] = q

    params["lat"] = lat

    params["lng"] = lng

    params["radius"] = radius

    params["language"] = language

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/offers/search",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list[OfferSearchResultDto] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OfferSearchResultDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[OfferSearchResultDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    q: str,
    lat: float,
    lng: float,
    radius: float | Unset = 10000.0,
    language: str | Unset = UNSET,
) -> Response[list[OfferSearchResultDto]]:
    """Search offers by title/brand near a point

    Args:
        q (str):
        lat (float):
        lng (float):
        radius (float | Unset):  Default: 10000.0.
        language (str | Unset):  Example: de-DE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[OfferSearchResultDto]]
    """

    kwargs = _get_kwargs(
        q=q,
        lat=lat,
        lng=lng,
        radius=radius,
        language=language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    q: str,
    lat: float,
    lng: float,
    radius: float | Unset = 10000.0,
    language: str | Unset = UNSET,
) -> list[OfferSearchResultDto] | None:
    """Search offers by title/brand near a point

    Args:
        q (str):
        lat (float):
        lng (float):
        radius (float | Unset):  Default: 10000.0.
        language (str | Unset):  Example: de-DE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[OfferSearchResultDto]
    """

    return sync_detailed(
        client=client,
        q=q,
        lat=lat,
        lng=lng,
        radius=radius,
        language=language,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    q: str,
    lat: float,
    lng: float,
    radius: float | Unset = 10000.0,
    language: str | Unset = UNSET,
) -> Response[list[OfferSearchResultDto]]:
    """Search offers by title/brand near a point

    Args:
        q (str):
        lat (float):
        lng (float):
        radius (float | Unset):  Default: 10000.0.
        language (str | Unset):  Example: de-DE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[OfferSearchResultDto]]
    """

    kwargs = _get_kwargs(
        q=q,
        lat=lat,
        lng=lng,
        radius=radius,
        language=language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    q: str,
    lat: float,
    lng: float,
    radius: float | Unset = 10000.0,
    language: str | Unset = UNSET,
) -> list[OfferSearchResultDto] | None:
    """Search offers by title/brand near a point

    Args:
        q (str):
        lat (float):
        lng (float):
        radius (float | Unset):  Default: 10000.0.
        language (str | Unset):  Example: de-DE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[OfferSearchResultDto]
    """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            lat=lat,
            lng=lng,
            radius=radius,
            language=language,
        )
    ).parsed
