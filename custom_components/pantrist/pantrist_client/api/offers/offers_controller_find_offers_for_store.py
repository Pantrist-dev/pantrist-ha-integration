from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.store_offers_dto import StoreOffersDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    store_id: str,
    *,
    language: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["language"] = language

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/offers/stores/{store_id}".format(
            store_id=quote(str(store_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> StoreOffersDto | None:
    if response.status_code == 200:
        response_200 = StoreOffersDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[StoreOffersDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient,
    language: str | Unset = UNSET,
) -> Response[StoreOffersDto]:
    """Current week's offers for one market

    Args:
        store_id (str):
        language (str | Unset):  Example: de-DE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StoreOffersDto]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        language=language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    store_id: str,
    *,
    client: AuthenticatedClient,
    language: str | Unset = UNSET,
) -> StoreOffersDto | None:
    """Current week's offers for one market

    Args:
        store_id (str):
        language (str | Unset):  Example: de-DE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StoreOffersDto
    """

    return sync_detailed(
        store_id=store_id,
        client=client,
        language=language,
    ).parsed


async def asyncio_detailed(
    store_id: str,
    *,
    client: AuthenticatedClient,
    language: str | Unset = UNSET,
) -> Response[StoreOffersDto]:
    """Current week's offers for one market

    Args:
        store_id (str):
        language (str | Unset):  Example: de-DE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StoreOffersDto]
    """

    kwargs = _get_kwargs(
        store_id=store_id,
        language=language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    store_id: str,
    *,
    client: AuthenticatedClient,
    language: str | Unset = UNSET,
) -> StoreOffersDto | None:
    """Current week's offers for one market

    Args:
        store_id (str):
        language (str | Unset):  Example: de-DE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StoreOffersDto
    """

    return (
        await asyncio_detailed(
            store_id=store_id,
            client=client,
            language=language,
        )
    ).parsed
