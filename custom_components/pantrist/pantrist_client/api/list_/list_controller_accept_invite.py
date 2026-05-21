from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_dto import ListDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    token: str,
    *,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/list/invites/{token}/accept".format(
            token=quote(str(token), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ListDto | None:
    if response.status_code == 201:
        response_201 = ListDto.from_dict(response.json())

        return response_201

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ListDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    token: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> Response[ListDto]:
    """Accept a share-link invite. The caller is added as a member at the invite role.

    Args:
        token (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListDto]
    """

    kwargs = _get_kwargs(
        token=token,
        x_socket_id=x_socket_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    token: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> ListDto | None:
    """Accept a share-link invite. The caller is added as a member at the invite role.

    Args:
        token (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListDto
    """

    return sync_detailed(
        token=token,
        client=client,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    token: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> Response[ListDto]:
    """Accept a share-link invite. The caller is added as a member at the invite role.

    Args:
        token (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListDto]
    """

    kwargs = _get_kwargs(
        token=token,
        x_socket_id=x_socket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    token: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> ListDto | None:
    """Accept a share-link invite. The caller is added as a member at the invite role.

    Args:
        token (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListDto
    """

    return (
        await asyncio_detailed(
            token=token,
            client=client,
            x_socket_id=x_socket_id,
        )
    ).parsed
