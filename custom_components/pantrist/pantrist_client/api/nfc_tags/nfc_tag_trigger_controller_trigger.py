from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.article_dto import ArticleDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    tag_id: str,
    *,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/nfc/tags/{tag_id}/trigger".format(
            tag_id=quote(str(tag_id), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ArticleDto | None:
    if response.status_code == 201:
        response_201 = ArticleDto.from_dict(response.json())

        return response_201

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ArticleDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tag_id: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> Response[ArticleDto]:
    """Trigger an NFC tag: deplete its mapped article

    Args:
        tag_id (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArticleDto]
    """

    kwargs = _get_kwargs(
        tag_id=tag_id,
        x_socket_id=x_socket_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tag_id: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> ArticleDto | None:
    """Trigger an NFC tag: deplete its mapped article

    Args:
        tag_id (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ArticleDto
    """

    return sync_detailed(
        tag_id=tag_id,
        client=client,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    tag_id: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> Response[ArticleDto]:
    """Trigger an NFC tag: deplete its mapped article

    Args:
        tag_id (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArticleDto]
    """

    kwargs = _get_kwargs(
        tag_id=tag_id,
        x_socket_id=x_socket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tag_id: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> ArticleDto | None:
    """Trigger an NFC tag: deplete its mapped article

    Args:
        tag_id (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ArticleDto
    """

    return (
        await asyncio_detailed(
            tag_id=tag_id,
            client=client,
            x_socket_id=x_socket_id,
        )
    ).parsed
