from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.article_dto import ArticleDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    item_id: str,
    source_list_id: str,
    *,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/list/{list_id}/shoppingList/{item_id}/move-from/{source_list_id}".format(
            list_id=quote(str(list_id), safe=""),
            item_id=quote(str(item_id), safe=""),
            source_list_id=quote(str(source_list_id), safe=""),
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
    list_id: str,
    item_id: str,
    source_list_id: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> Response[ArticleDto]:
    """Move an item into the shopping list

    Args:
        list_id (str):
        item_id (str):
        source_list_id (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArticleDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        item_id=item_id,
        source_list_id=source_list_id,
        x_socket_id=x_socket_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    item_id: str,
    source_list_id: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> ArticleDto | None:
    """Move an item into the shopping list

    Args:
        list_id (str):
        item_id (str):
        source_list_id (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ArticleDto
    """

    return sync_detailed(
        list_id=list_id,
        item_id=item_id,
        source_list_id=source_list_id,
        client=client,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    item_id: str,
    source_list_id: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> Response[ArticleDto]:
    """Move an item into the shopping list

    Args:
        list_id (str):
        item_id (str):
        source_list_id (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArticleDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        item_id=item_id,
        source_list_id=source_list_id,
        x_socket_id=x_socket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    item_id: str,
    source_list_id: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> ArticleDto | None:
    """Move an item into the shopping list

    Args:
        list_id (str):
        item_id (str):
        source_list_id (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ArticleDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            item_id=item_id,
            source_list_id=source_list_id,
            client=client,
            x_socket_id=x_socket_id,
        )
    ).parsed
