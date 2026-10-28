from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.access_token_response_dto import AccessTokenResponseDto
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/token/renew",
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AccessTokenResponseDto | None:
    if response.status_code == 200:
        response_200 = AccessTokenResponseDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AccessTokenResponseDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[AccessTokenResponseDto]:
    """Get a fresh access token from a (possibly expired) session access token

     For the native widgets, which only hold the access token the app mirrored into shared storage. Works
    as long as the underlying session has not been revoked or expired.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccessTokenResponseDto]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> AccessTokenResponseDto | None:
    """Get a fresh access token from a (possibly expired) session access token

     For the native widgets, which only hold the access token the app mirrored into shared storage. Works
    as long as the underlying session has not been revoked or expired.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccessTokenResponseDto
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[AccessTokenResponseDto]:
    """Get a fresh access token from a (possibly expired) session access token

     For the native widgets, which only hold the access token the app mirrored into shared storage. Works
    as long as the underlying session has not been revoked or expired.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccessTokenResponseDto]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> AccessTokenResponseDto | None:
    """Get a fresh access token from a (possibly expired) session access token

     For the native widgets, which only hold the access token the app mirrored into shared storage. Works
    as long as the underlying session has not been revoked or expired.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccessTokenResponseDto
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
