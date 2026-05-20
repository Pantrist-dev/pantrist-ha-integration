from http import HTTPStatus
from typing import Any, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_recipe_collections_with_images_dto import GetRecipeCollectionsWithImagesDto
from ...models.recipe_collection_controller_get_collections_type import RecipeCollectionControllerGetCollectionsType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    search_text: str | Unset = UNSET,
    type_: RecipeCollectionControllerGetCollectionsType | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["searchText"] = search_text

    json_type_: str | Unset = UNSET
    if not isinstance(type_, Unset):
        json_type_ = type_.value

    params["type"] = json_type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/recipe-collection",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | list[GetRecipeCollectionsWithImagesDto] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetRecipeCollectionsWithImagesDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Any | list[GetRecipeCollectionsWithImagesDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    search_text: str | Unset = UNSET,
    type_: RecipeCollectionControllerGetCollectionsType | Unset = UNSET,
) -> Response[Any | list[GetRecipeCollectionsWithImagesDto]]:
    """Get recipe collections of the current user

     Returns all recipe collections of the authenticated user. Supports filtering by type and search
    text.

    Args:
        search_text (str | Unset):
        type_ (RecipeCollectionControllerGetCollectionsType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | list[GetRecipeCollectionsWithImagesDto]]
    """

    kwargs = _get_kwargs(
        search_text=search_text,
        type_=type_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    search_text: str | Unset = UNSET,
    type_: RecipeCollectionControllerGetCollectionsType | Unset = UNSET,
) -> Any | list[GetRecipeCollectionsWithImagesDto] | None:
    """Get recipe collections of the current user

     Returns all recipe collections of the authenticated user. Supports filtering by type and search
    text.

    Args:
        search_text (str | Unset):
        type_ (RecipeCollectionControllerGetCollectionsType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | list[GetRecipeCollectionsWithImagesDto]
    """

    return sync_detailed(
        client=client,
        search_text=search_text,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    search_text: str | Unset = UNSET,
    type_: RecipeCollectionControllerGetCollectionsType | Unset = UNSET,
) -> Response[Any | list[GetRecipeCollectionsWithImagesDto]]:
    """Get recipe collections of the current user

     Returns all recipe collections of the authenticated user. Supports filtering by type and search
    text.

    Args:
        search_text (str | Unset):
        type_ (RecipeCollectionControllerGetCollectionsType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | list[GetRecipeCollectionsWithImagesDto]]
    """

    kwargs = _get_kwargs(
        search_text=search_text,
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    search_text: str | Unset = UNSET,
    type_: RecipeCollectionControllerGetCollectionsType | Unset = UNSET,
) -> Any | list[GetRecipeCollectionsWithImagesDto] | None:
    """Get recipe collections of the current user

     Returns all recipe collections of the authenticated user. Supports filtering by type and search
    text.

    Args:
        search_text (str | Unset):
        type_ (RecipeCollectionControllerGetCollectionsType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | list[GetRecipeCollectionsWithImagesDto]
    """

    return (
        await asyncio_detailed(
            client=client,
            search_text=search_text,
            type_=type_,
        )
    ).parsed
