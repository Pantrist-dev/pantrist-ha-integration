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
    *,
    body: ArticleDto,
    auto_restock: bool | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    params: dict[str, Any] = {}

    params["autoRestock"] = auto_restock

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/list/{list_id}/pantryList/{item_id}".format(
            list_id=quote(str(list_id), safe=""),
            item_id=quote(str(item_id), safe=""),
        ),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ArticleDto | None:
    if response.status_code == 200:
        response_200 = ArticleDto.from_dict(response.json())

        return response_200

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
    *,
    client: AuthenticatedClient,
    body: ArticleDto,
    auto_restock: bool | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> Response[ArticleDto]:
    """Add or update a pantry list item

    Args:
        list_id (str):
        item_id (str):
        auto_restock (bool | Unset):
        x_socket_id (str | Unset):
        body (ArticleDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArticleDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        item_id=item_id,
        body=body,
        auto_restock=auto_restock,
        x_socket_id=x_socket_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
    body: ArticleDto,
    auto_restock: bool | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> ArticleDto | None:
    """Add or update a pantry list item

    Args:
        list_id (str):
        item_id (str):
        auto_restock (bool | Unset):
        x_socket_id (str | Unset):
        body (ArticleDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ArticleDto
    """

    return sync_detailed(
        list_id=list_id,
        item_id=item_id,
        client=client,
        body=body,
        auto_restock=auto_restock,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
    body: ArticleDto,
    auto_restock: bool | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> Response[ArticleDto]:
    """Add or update a pantry list item

    Args:
        list_id (str):
        item_id (str):
        auto_restock (bool | Unset):
        x_socket_id (str | Unset):
        body (ArticleDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArticleDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        item_id=item_id,
        body=body,
        auto_restock=auto_restock,
        x_socket_id=x_socket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
    body: ArticleDto,
    auto_restock: bool | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> ArticleDto | None:
    """Add or update a pantry list item

    Args:
        list_id (str):
        item_id (str):
        auto_restock (bool | Unset):
        x_socket_id (str | Unset):
        body (ArticleDto):

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
            client=client,
            body=body,
            auto_restock=auto_restock,
            x_socket_id=x_socket_id,
        )
    ).parsed
