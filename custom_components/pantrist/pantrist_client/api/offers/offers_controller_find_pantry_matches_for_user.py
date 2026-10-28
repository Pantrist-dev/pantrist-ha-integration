from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.pantry_offer_match_dto import PantryOfferMatchDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    *,
    language: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["language"] = language

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/offers/list/{list_id}/pantry-matches".format(
            list_id=quote(str(list_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list[PantryOfferMatchDto] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PantryOfferMatchDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[PantryOfferMatchDto]]:
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
    language: str | Unset = UNSET,
) -> Response[list[PantryOfferMatchDto]]:
    """Pantry items on this list with a minimum stock tracked that currently have a matching offer at one
    of the caller's home markets, cheapest one per item.

    Args:
        list_id (str):
        language (str | Unset):  Example: de-DE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[PantryOfferMatchDto]]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        language=language,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    *,
    client: AuthenticatedClient,
    language: str | Unset = UNSET,
) -> list[PantryOfferMatchDto] | None:
    """Pantry items on this list with a minimum stock tracked that currently have a matching offer at one
    of the caller's home markets, cheapest one per item.

    Args:
        list_id (str):
        language (str | Unset):  Example: de-DE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[PantryOfferMatchDto]
    """

    return sync_detailed(
        list_id=list_id,
        client=client,
        language=language,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    *,
    client: AuthenticatedClient,
    language: str | Unset = UNSET,
) -> Response[list[PantryOfferMatchDto]]:
    """Pantry items on this list with a minimum stock tracked that currently have a matching offer at one
    of the caller's home markets, cheapest one per item.

    Args:
        list_id (str):
        language (str | Unset):  Example: de-DE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[PantryOfferMatchDto]]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        language=language,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    *,
    client: AuthenticatedClient,
    language: str | Unset = UNSET,
) -> list[PantryOfferMatchDto] | None:
    """Pantry items on this list with a minimum stock tracked that currently have a matching offer at one
    of the caller's home markets, cheapest one per item.

    Args:
        list_id (str):
        language (str | Unset):  Example: de-DE.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[PantryOfferMatchDto]
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            client=client,
            language=language,
        )
    ).parsed
