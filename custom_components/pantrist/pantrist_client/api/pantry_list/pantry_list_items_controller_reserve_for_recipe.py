from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.article_dto import ArticleDto
from ...models.reserve_for_recipe_dto import ReserveForRecipeDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    item_id: str,
    recipe_uuid: str,
    *,
    body: ReserveForRecipeDto,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/list/{list_id}/pantryList/{item_id}/reservations/{recipe_uuid}".format(
            list_id=quote(str(list_id), safe=""),
            item_id=quote(str(item_id), safe=""),
            recipe_uuid=quote(str(recipe_uuid), safe=""),
        ),
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
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    body: ReserveForRecipeDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[ArticleDto]:
    """Reserve stock of a pantry item for a recipe

     Sets stock aside in `pantrySettings.savedForRecipe` until the recipe is cooked, replacing this
    item's earlier reservation for the same recipe. `recipeUuid` is a Pantrist recipe uuid, or an id of
    the caller's choosing plus a `recipeName` for a recipe that only exists outside of Pantrist.

    Args:
        list_id (str):
        item_id (str):
        recipe_uuid (str):
        x_socket_id (str | Unset):
        body (ReserveForRecipeDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArticleDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        item_id=item_id,
        recipe_uuid=recipe_uuid,
        body=body,
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
    body: ReserveForRecipeDto,
    x_socket_id: str | Unset = UNSET,
) -> ArticleDto | None:
    """Reserve stock of a pantry item for a recipe

     Sets stock aside in `pantrySettings.savedForRecipe` until the recipe is cooked, replacing this
    item's earlier reservation for the same recipe. `recipeUuid` is a Pantrist recipe uuid, or an id of
    the caller's choosing plus a `recipeName` for a recipe that only exists outside of Pantrist.

    Args:
        list_id (str):
        item_id (str):
        recipe_uuid (str):
        x_socket_id (str | Unset):
        body (ReserveForRecipeDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ArticleDto
    """

    return sync_detailed(
        list_id=list_id,
        item_id=item_id,
        recipe_uuid=recipe_uuid,
        client=client,
        body=body,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    item_id: str,
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    body: ReserveForRecipeDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[ArticleDto]:
    """Reserve stock of a pantry item for a recipe

     Sets stock aside in `pantrySettings.savedForRecipe` until the recipe is cooked, replacing this
    item's earlier reservation for the same recipe. `recipeUuid` is a Pantrist recipe uuid, or an id of
    the caller's choosing plus a `recipeName` for a recipe that only exists outside of Pantrist.

    Args:
        list_id (str):
        item_id (str):
        recipe_uuid (str):
        x_socket_id (str | Unset):
        body (ReserveForRecipeDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ArticleDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        item_id=item_id,
        recipe_uuid=recipe_uuid,
        body=body,
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
    body: ReserveForRecipeDto,
    x_socket_id: str | Unset = UNSET,
) -> ArticleDto | None:
    """Reserve stock of a pantry item for a recipe

     Sets stock aside in `pantrySettings.savedForRecipe` until the recipe is cooked, replacing this
    item's earlier reservation for the same recipe. `recipeUuid` is a Pantrist recipe uuid, or an id of
    the caller's choosing plus a `recipeName` for a recipe that only exists outside of Pantrist.

    Args:
        list_id (str):
        item_id (str):
        recipe_uuid (str):
        x_socket_id (str | Unset):
        body (ReserveForRecipeDto):

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
            recipe_uuid=recipe_uuid,
            client=client,
            body=body,
            x_socket_id=x_socket_id,
        )
    ).parsed
