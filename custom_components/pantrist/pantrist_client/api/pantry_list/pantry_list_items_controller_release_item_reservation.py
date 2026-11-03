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
    recipe_uuid: str,
    *,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/list/{list_id}/pantryList/{item_id}/reservations/{recipe_uuid}".format(
            list_id=quote(str(list_id), safe=""),
            item_id=quote(str(item_id), safe=""),
            recipe_uuid=quote(str(recipe_uuid), safe=""),
        ),
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> list[ArticleDto] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ArticleDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[list[ArticleDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    list_id: str,
    item_id: str,
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> Response[list[ArticleDto]]:
    """Release one pantry item's reservation for a recipe

     Nothing is booked out of the stock.

    Args:
        list_id (str):
        item_id (str):
        recipe_uuid (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[ArticleDto]]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        item_id=item_id,
        recipe_uuid=recipe_uuid,
        x_socket_id=x_socket_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    item_id: str,
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> list[ArticleDto] | None:
    """Release one pantry item's reservation for a recipe

     Nothing is booked out of the stock.

    Args:
        list_id (str):
        item_id (str):
        recipe_uuid (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[ArticleDto]
    """

    return sync_detailed(
        list_id=list_id,
        item_id=item_id,
        recipe_uuid=recipe_uuid,
        client=client,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    item_id: str,
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> Response[list[ArticleDto]]:
    """Release one pantry item's reservation for a recipe

     Nothing is booked out of the stock.

    Args:
        list_id (str):
        item_id (str):
        recipe_uuid (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[ArticleDto]]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        item_id=item_id,
        recipe_uuid=recipe_uuid,
        x_socket_id=x_socket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    item_id: str,
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    x_socket_id: str | Unset = UNSET,
) -> list[ArticleDto] | None:
    """Release one pantry item's reservation for a recipe

     Nothing is booked out of the stock.

    Args:
        list_id (str):
        item_id (str):
        recipe_uuid (str):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[ArticleDto]
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            item_id=item_id,
            recipe_uuid=recipe_uuid,
            client=client,
            x_socket_id=x_socket_id,
        )
    ).parsed
