from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.recipe_deck_request_dto import RecipeDeckRequestDto
from ...models.recipe_dto import RecipeDto
from ...types import Response


def _get_kwargs(
    *,
    body: RecipeDeckRequestDto,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/recipe/swipe/deck",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> list[RecipeDto] | None:
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = RecipeDto.from_dict(response_201_item_data)

            response_201.append(response_201_item)

        return response_201

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[list[RecipeDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: RecipeDeckRequestDto,
) -> Response[list[RecipeDto]]:
    """Get a randomised deck of recipes the user has not swiped yet

     Returns fresh cards every call: recipes the user has already liked are excluded forever and recipes
    they skipped are excluded for a recycle window, so planning sessions keep surfacing different
    recipes. Accepts the full recipe filter (dietaryStyles, excludeAllergens, ingredients/pantry,
    language, time, …). Browseable without an account; when a token *is* supplied the deck personalises
    (excludes already-swiped recipes, applies pantry hydration).

    Args:
        body (RecipeDeckRequestDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[RecipeDto]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: RecipeDeckRequestDto,
) -> list[RecipeDto] | None:
    """Get a randomised deck of recipes the user has not swiped yet

     Returns fresh cards every call: recipes the user has already liked are excluded forever and recipes
    they skipped are excluded for a recycle window, so planning sessions keep surfacing different
    recipes. Accepts the full recipe filter (dietaryStyles, excludeAllergens, ingredients/pantry,
    language, time, …). Browseable without an account; when a token *is* supplied the deck personalises
    (excludes already-swiped recipes, applies pantry hydration).

    Args:
        body (RecipeDeckRequestDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[RecipeDto]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: RecipeDeckRequestDto,
) -> Response[list[RecipeDto]]:
    """Get a randomised deck of recipes the user has not swiped yet

     Returns fresh cards every call: recipes the user has already liked are excluded forever and recipes
    they skipped are excluded for a recycle window, so planning sessions keep surfacing different
    recipes. Accepts the full recipe filter (dietaryStyles, excludeAllergens, ingredients/pantry,
    language, time, …). Browseable without an account; when a token *is* supplied the deck personalises
    (excludes already-swiped recipes, applies pantry hydration).

    Args:
        body (RecipeDeckRequestDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[RecipeDto]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: RecipeDeckRequestDto,
) -> list[RecipeDto] | None:
    """Get a randomised deck of recipes the user has not swiped yet

     Returns fresh cards every call: recipes the user has already liked are excluded forever and recipes
    they skipped are excluded for a recycle window, so planning sessions keep surfacing different
    recipes. Accepts the full recipe filter (dietaryStyles, excludeAllergens, ingredients/pantry,
    language, time, …). Browseable without an account; when a token *is* supplied the deck personalises
    (excludes already-swiped recipes, applies pantry hydration).

    Args:
        body (RecipeDeckRequestDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[RecipeDto]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
