from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.loyalty_card_dto import LoyaltyCardDto
from ...models.upsert_loyalty_card_dto import UpsertLoyaltyCardDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: str,
    *,
    body: UpsertLoyaltyCardDto,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/loyalty-cards/{uuid}".format(
            uuid=quote(str(uuid), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> LoyaltyCardDto | None:
    if response.status_code == 200:
        response_200 = LoyaltyCardDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[LoyaltyCardDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: str,
    *,
    client: AuthenticatedClient,
    body: UpsertLoyaltyCardDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[LoyaltyCardDto]:
    """Create or update one of the caller's cards

    Args:
        uuid (str):
        x_socket_id (str | Unset):
        body (UpsertLoyaltyCardDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LoyaltyCardDto]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
        x_socket_id=x_socket_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: str,
    *,
    client: AuthenticatedClient,
    body: UpsertLoyaltyCardDto,
    x_socket_id: str | Unset = UNSET,
) -> LoyaltyCardDto | None:
    """Create or update one of the caller's cards

    Args:
        uuid (str):
        x_socket_id (str | Unset):
        body (UpsertLoyaltyCardDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LoyaltyCardDto
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    uuid: str,
    *,
    client: AuthenticatedClient,
    body: UpsertLoyaltyCardDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[LoyaltyCardDto]:
    """Create or update one of the caller's cards

    Args:
        uuid (str):
        x_socket_id (str | Unset):
        body (UpsertLoyaltyCardDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[LoyaltyCardDto]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
        x_socket_id=x_socket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: str,
    *,
    client: AuthenticatedClient,
    body: UpsertLoyaltyCardDto,
    x_socket_id: str | Unset = UNSET,
) -> LoyaltyCardDto | None:
    """Create or update one of the caller's cards

    Args:
        uuid (str):
        x_socket_id (str | Unset):
        body (UpsertLoyaltyCardDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        LoyaltyCardDto
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
            x_socket_id=x_socket_id,
        )
    ).parsed
