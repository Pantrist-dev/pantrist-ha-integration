from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.article_dto import ArticleDto
from ...models.success_dto import SuccessDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: ArticleDto,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/shopping-cart",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> SuccessDto:
    response_default = SuccessDto.from_dict(response.json())

    return response_default


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[SuccessDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ArticleDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[SuccessDto]:
    """Add an item to the shopping cart

    Args:
        x_socket_id (str | Unset):
        body (ArticleDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SuccessDto]
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
    body: ArticleDto,
    x_socket_id: str | Unset = UNSET,
) -> SuccessDto | None:
    """Add an item to the shopping cart

    Args:
        x_socket_id (str | Unset):
        body (ArticleDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SuccessDto
    """

    return sync_detailed(
        client=client,
        body=body,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ArticleDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[SuccessDto]:
    """Add an item to the shopping cart

    Args:
        x_socket_id (str | Unset):
        body (ArticleDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SuccessDto]
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
    body: ArticleDto,
    x_socket_id: str | Unset = UNSET,
) -> SuccessDto | None:
    """Add an item to the shopping cart

    Args:
        x_socket_id (str | Unset):
        body (ArticleDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SuccessDto
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            x_socket_id=x_socket_id,
        )
    ).parsed
