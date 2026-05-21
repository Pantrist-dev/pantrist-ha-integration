from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.premium_invitation_dto import PremiumInvitationDto
from ...models.sync_firebase_invitation_dto import SyncFirebaseInvitationDto
from ...types import Response


def _get_kwargs(
    inviter_id: str,
    *,
    body: SyncFirebaseInvitationDto,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/premium-invitations/{inviter_id}/sync".format(
            inviter_id=quote(str(inviter_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | PremiumInvitationDto | None:
    if response.status_code == 200:
        response_200 = PremiumInvitationDto.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | PremiumInvitationDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    inviter_id: str,
    *,
    client: AuthenticatedClient,
    body: SyncFirebaseInvitationDto,
) -> Response[Any | PremiumInvitationDto]:
    """Sync Firebase invitation data (update)

     Update invitation based on Firebase data for a specific inviter.

    Args:
        inviter_id (str):
        body (SyncFirebaseInvitationDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PremiumInvitationDto]
    """

    kwargs = _get_kwargs(
        inviter_id=inviter_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    inviter_id: str,
    *,
    client: AuthenticatedClient,
    body: SyncFirebaseInvitationDto,
) -> Any | PremiumInvitationDto | None:
    """Sync Firebase invitation data (update)

     Update invitation based on Firebase data for a specific inviter.

    Args:
        inviter_id (str):
        body (SyncFirebaseInvitationDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PremiumInvitationDto
    """

    return sync_detailed(
        inviter_id=inviter_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    inviter_id: str,
    *,
    client: AuthenticatedClient,
    body: SyncFirebaseInvitationDto,
) -> Response[Any | PremiumInvitationDto]:
    """Sync Firebase invitation data (update)

     Update invitation based on Firebase data for a specific inviter.

    Args:
        inviter_id (str):
        body (SyncFirebaseInvitationDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | PremiumInvitationDto]
    """

    kwargs = _get_kwargs(
        inviter_id=inviter_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    inviter_id: str,
    *,
    client: AuthenticatedClient,
    body: SyncFirebaseInvitationDto,
) -> Any | PremiumInvitationDto | None:
    """Sync Firebase invitation data (update)

     Update invitation based on Firebase data for a specific inviter.

    Args:
        inviter_id (str):
        body (SyncFirebaseInvitationDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | PremiumInvitationDto
    """

    return (
        await asyncio_detailed(
            inviter_id=inviter_id,
            client=client,
            body=body,
        )
    ).parsed
