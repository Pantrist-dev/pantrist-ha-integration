from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.auth_rollout_dto import AuthRolloutDto
from ...types import Response


def _get_kwargs() -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/auth/rollout",
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthRolloutDto | None:
    if response.status_code == 200:
        response_200 = AuthRolloutDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthRolloutDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[AuthRolloutDto]:
    """Is self-hosted sign-in enabled for the caller?

     Send the current bearer token (Firebase ID token or Pantrist access token) to get a per-user answer;
    without a usable token only the global mode is reported. The app uses this to choose between the
    Firebase and the Pantrist auth backend during the migration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthRolloutDto]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> AuthRolloutDto | None:
    """Is self-hosted sign-in enabled for the caller?

     Send the current bearer token (Firebase ID token or Pantrist access token) to get a per-user answer;
    without a usable token only the global mode is reported. The app uses this to choose between the
    Firebase and the Pantrist auth backend during the migration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthRolloutDto
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[AuthRolloutDto]:
    """Is self-hosted sign-in enabled for the caller?

     Send the current bearer token (Firebase ID token or Pantrist access token) to get a per-user answer;
    without a usable token only the global mode is reported. The app uses this to choose between the
    Firebase and the Pantrist auth backend during the migration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthRolloutDto]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> AuthRolloutDto | None:
    """Is self-hosted sign-in enabled for the caller?

     Send the current bearer token (Firebase ID token or Pantrist access token) to get a per-user answer;
    without a usable token only the global mode is reported. The app uses this to choose between the
    Firebase and the Pantrist auth backend during the migration.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthRolloutDto
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
