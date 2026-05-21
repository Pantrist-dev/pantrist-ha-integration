from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.access_token_controller_authorize_code_challenge_method import (
    AccessTokenControllerAuthorizeCodeChallengeMethod,
)
from ...models.access_token_controller_authorize_response_200 import AccessTokenControllerAuthorizeResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    response_type: str,
    client_id: str,
    redirect_uri: str,
    state: str,
    code_challenge: str | Unset = UNSET,
    code_challenge_method: AccessTokenControllerAuthorizeCodeChallengeMethod | Unset = UNSET,
    list_id: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["response_type"] = response_type

    params["client_id"] = client_id

    params["redirect_uri"] = redirect_uri

    params["state"] = state

    params["code_challenge"] = code_challenge

    json_code_challenge_method: str | Unset = UNSET
    if not isinstance(code_challenge_method, Unset):
        json_code_challenge_method = code_challenge_method.value

    params["code_challenge_method"] = json_code_challenge_method

    params["list_id"] = list_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/access-token/authorize",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> AccessTokenControllerAuthorizeResponse200 | Any | None:
    if response.status_code == 200:
        response_200 = AccessTokenControllerAuthorizeResponse200.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[AccessTokenControllerAuthorizeResponse200 | Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    response_type: str,
    client_id: str,
    redirect_uri: str,
    state: str,
    code_challenge: str | Unset = UNSET,
    code_challenge_method: AccessTokenControllerAuthorizeCodeChallengeMethod | Unset = UNSET,
    list_id: str | Unset = UNSET,
) -> Response[AccessTokenControllerAuthorizeResponse200 | Any]:
    """
    Args:
        response_type (str):
        client_id (str):
        redirect_uri (str):
        state (str):
        code_challenge (str | Unset):
        code_challenge_method (AccessTokenControllerAuthorizeCodeChallengeMethod | Unset):
        list_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccessTokenControllerAuthorizeResponse200 | Any]
    """

    kwargs = _get_kwargs(
        response_type=response_type,
        client_id=client_id,
        redirect_uri=redirect_uri,
        state=state,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        list_id=list_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    response_type: str,
    client_id: str,
    redirect_uri: str,
    state: str,
    code_challenge: str | Unset = UNSET,
    code_challenge_method: AccessTokenControllerAuthorizeCodeChallengeMethod | Unset = UNSET,
    list_id: str | Unset = UNSET,
) -> AccessTokenControllerAuthorizeResponse200 | Any | None:
    """
    Args:
        response_type (str):
        client_id (str):
        redirect_uri (str):
        state (str):
        code_challenge (str | Unset):
        code_challenge_method (AccessTokenControllerAuthorizeCodeChallengeMethod | Unset):
        list_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccessTokenControllerAuthorizeResponse200 | Any
    """

    return sync_detailed(
        client=client,
        response_type=response_type,
        client_id=client_id,
        redirect_uri=redirect_uri,
        state=state,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        list_id=list_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    response_type: str,
    client_id: str,
    redirect_uri: str,
    state: str,
    code_challenge: str | Unset = UNSET,
    code_challenge_method: AccessTokenControllerAuthorizeCodeChallengeMethod | Unset = UNSET,
    list_id: str | Unset = UNSET,
) -> Response[AccessTokenControllerAuthorizeResponse200 | Any]:
    """
    Args:
        response_type (str):
        client_id (str):
        redirect_uri (str):
        state (str):
        code_challenge (str | Unset):
        code_challenge_method (AccessTokenControllerAuthorizeCodeChallengeMethod | Unset):
        list_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccessTokenControllerAuthorizeResponse200 | Any]
    """

    kwargs = _get_kwargs(
        response_type=response_type,
        client_id=client_id,
        redirect_uri=redirect_uri,
        state=state,
        code_challenge=code_challenge,
        code_challenge_method=code_challenge_method,
        list_id=list_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    response_type: str,
    client_id: str,
    redirect_uri: str,
    state: str,
    code_challenge: str | Unset = UNSET,
    code_challenge_method: AccessTokenControllerAuthorizeCodeChallengeMethod | Unset = UNSET,
    list_id: str | Unset = UNSET,
) -> AccessTokenControllerAuthorizeResponse200 | Any | None:
    """
    Args:
        response_type (str):
        client_id (str):
        redirect_uri (str):
        state (str):
        code_challenge (str | Unset):
        code_challenge_method (AccessTokenControllerAuthorizeCodeChallengeMethod | Unset):
        list_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccessTokenControllerAuthorizeResponse200 | Any
    """

    return (
        await asyncio_detailed(
            client=client,
            response_type=response_type,
            client_id=client_id,
            redirect_uri=redirect_uri,
            state=state,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            list_id=list_id,
        )
    ).parsed
