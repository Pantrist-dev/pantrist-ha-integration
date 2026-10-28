from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.auth_controller_login_with_provider_provider import AuthControllerLoginWithProviderProvider
from ...models.auth_session_response_dto import AuthSessionResponseDto
from ...models.provider_login_dto import ProviderLoginDto
from ...types import Response


def _get_kwargs(
    provider: AuthControllerLoginWithProviderProvider,
    *,
    body: ProviderLoginDto,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/provider/{provider}".format(
            provider=quote(str(provider), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthSessionResponseDto | None:
    if response.status_code == 200:
        response_200 = AuthSessionResponseDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AuthSessionResponseDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider: AuthControllerLoginWithProviderProvider,
    *,
    client: AuthenticatedClient | Client,
    body: ProviderLoginDto,
) -> Response[AuthSessionResponseDto]:
    """Sign in (or up) with Google, Apple or Facebook

     Send the provider credential obtained on the device: `idToken` for google.com / apple.com,
    `accessToken` for facebook.com. A verified email that already belongs to an account links the
    identity to that account instead of creating a new one.

    Args:
        provider (AuthControllerLoginWithProviderProvider):
        body (ProviderLoginDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthSessionResponseDto]
    """

    kwargs = _get_kwargs(
        provider=provider,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    provider: AuthControllerLoginWithProviderProvider,
    *,
    client: AuthenticatedClient | Client,
    body: ProviderLoginDto,
) -> AuthSessionResponseDto | None:
    """Sign in (or up) with Google, Apple or Facebook

     Send the provider credential obtained on the device: `idToken` for google.com / apple.com,
    `accessToken` for facebook.com. A verified email that already belongs to an account links the
    identity to that account instead of creating a new one.

    Args:
        provider (AuthControllerLoginWithProviderProvider):
        body (ProviderLoginDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthSessionResponseDto
    """

    return sync_detailed(
        provider=provider,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    provider: AuthControllerLoginWithProviderProvider,
    *,
    client: AuthenticatedClient | Client,
    body: ProviderLoginDto,
) -> Response[AuthSessionResponseDto]:
    """Sign in (or up) with Google, Apple or Facebook

     Send the provider credential obtained on the device: `idToken` for google.com / apple.com,
    `accessToken` for facebook.com. A verified email that already belongs to an account links the
    identity to that account instead of creating a new one.

    Args:
        provider (AuthControllerLoginWithProviderProvider):
        body (ProviderLoginDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthSessionResponseDto]
    """

    kwargs = _get_kwargs(
        provider=provider,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    provider: AuthControllerLoginWithProviderProvider,
    *,
    client: AuthenticatedClient | Client,
    body: ProviderLoginDto,
) -> AuthSessionResponseDto | None:
    """Sign in (or up) with Google, Apple or Facebook

     Send the provider credential obtained on the device: `idToken` for google.com / apple.com,
    `accessToken` for facebook.com. A verified email that already belongs to an account links the
    identity to that account instead of creating a new one.

    Args:
        provider (AuthControllerLoginWithProviderProvider):
        body (ProviderLoginDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthSessionResponseDto
    """

    return (
        await asyncio_detailed(
            provider=provider,
            client=client,
            body=body,
        )
    ).parsed
