from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.add_by_name_dto import AddByNameDto
from ...models.article_dto import ArticleDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: AddByNameDto,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/shopping-list/add-by-name",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ArticleDto:
    response_default = ArticleDto.from_dict(response.json())

    return response_default


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ArticleDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AddByNameDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[ArticleDto]:
    """Adds an item to the shopping list by its name

     Use POST /list/:listId/shoppingList/add-by-name instead.

    Args:
        x_socket_id (str | Unset):
        body (AddByNameDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArticleDto]
    """

    kwargs = _get_kwargs(
        body=body,
        x_socket_id=x_socket_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: AddByNameDto,
    x_socket_id: str | Unset = UNSET,
) -> ArticleDto | None:
    """Adds an item to the shopping list by its name

     Use POST /list/:listId/shoppingList/add-by-name instead.

    Args:
        x_socket_id (str | Unset):
        body (AddByNameDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ArticleDto
    """

    return sync_detailed(
        client=client,
        body=body,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AddByNameDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[ArticleDto]:
    """Adds an item to the shopping list by its name

     Use POST /list/:listId/shoppingList/add-by-name instead.

    Args:
        x_socket_id (str | Unset):
        body (AddByNameDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArticleDto]
    """

    kwargs = _get_kwargs(
        body=body,
        x_socket_id=x_socket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AddByNameDto,
    x_socket_id: str | Unset = UNSET,
) -> ArticleDto | None:
    """Adds an item to the shopping list by its name

     Use POST /list/:listId/shoppingList/add-by-name instead.

    Args:
        x_socket_id (str | Unset):
        body (AddByNameDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ArticleDto
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_socket_id=x_socket_id,
        )
    ).parsed
