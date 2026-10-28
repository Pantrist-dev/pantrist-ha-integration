from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offer_recipe_ideas_controller_find_categories_item import OfferRecipeIdeasControllerFindCategoriesItem
from ...models.offer_recipe_ideas_controller_find_dietary_styles_item import (
    OfferRecipeIdeasControllerFindDietaryStylesItem,
)
from ...models.offer_recipe_ideas_controller_find_exclude_allergens_item import (
    OfferRecipeIdeasControllerFindExcludeAllergensItem,
)
from ...models.offer_recipe_ideas_response_dto import OfferRecipeIdeasResponseDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    store_ids: list[str] | Unset = UNSET,
    limit: float | Unset = UNSET,
    language: str | Unset = UNSET,
    categories: list[OfferRecipeIdeasControllerFindCategoriesItem] | Unset = UNSET,
    dietary_styles: list[OfferRecipeIdeasControllerFindDietaryStylesItem] | Unset = UNSET,
    exclude_allergens: list[OfferRecipeIdeasControllerFindExcludeAllergensItem] | Unset = UNSET,
    servings: float | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_store_ids: list[str] | Unset = UNSET
    if not isinstance(store_ids, Unset):
        json_store_ids = store_ids

    params["storeIds"] = json_store_ids

    params["limit"] = limit

    params["language"] = language

    json_categories: list[str] | Unset = UNSET
    if not isinstance(categories, Unset):
        json_categories = []
        for categories_item_data in categories:
            categories_item = categories_item_data.value
            json_categories.append(categories_item)

    params["categories"] = json_categories

    json_dietary_styles: list[str] | Unset = UNSET
    if not isinstance(dietary_styles, Unset):
        json_dietary_styles = []
        for dietary_styles_item_data in dietary_styles:
            dietary_styles_item = dietary_styles_item_data.value
            json_dietary_styles.append(dietary_styles_item)

    params["dietaryStyles"] = json_dietary_styles

    json_exclude_allergens: list[str] | Unset = UNSET
    if not isinstance(exclude_allergens, Unset):
        json_exclude_allergens = []
        for exclude_allergens_item_data in exclude_allergens:
            exclude_allergens_item = exclude_allergens_item_data.value
            json_exclude_allergens.append(exclude_allergens_item)

    params["excludeAllergens"] = json_exclude_allergens

    params["servings"] = servings

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/offers/recipe-ideas",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> OfferRecipeIdeasResponseDto | None:
    if response.status_code == 200:
        response_200 = OfferRecipeIdeasResponseDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[OfferRecipeIdeasResponseDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    store_ids: list[str] | Unset = UNSET,
    limit: float | Unset = UNSET,
    language: str | Unset = UNSET,
    categories: list[OfferRecipeIdeasControllerFindCategoriesItem] | Unset = UNSET,
    dietary_styles: list[OfferRecipeIdeasControllerFindDietaryStylesItem] | Unset = UNSET,
    exclude_allergens: list[OfferRecipeIdeasControllerFindExcludeAllergensItem] | Unset = UNSET,
    servings: float | Unset = UNSET,
) -> Response[OfferRecipeIdeasResponseDto]:
    """Recipes whose ingredients are on offer at the caller’s markets

     Ranked by how much of the shopping list is covered right now. The recipes are AI-generated and
    permanently flagged as such; the prices are computed per request from the offers currently on the
    shelf, so they change rather than expire. An empty `ideas` array with `offeredIngredientCount: 0` is
    the "nothing useful this week" case, not an error.

    Args:
        store_ids (list[str] | Unset):
        limit (float | Unset):
        language (str | Unset):
        categories (list[OfferRecipeIdeasControllerFindCategoriesItem] | Unset):
        dietary_styles (list[OfferRecipeIdeasControllerFindDietaryStylesItem] | Unset):
        exclude_allergens (list[OfferRecipeIdeasControllerFindExcludeAllergensItem] | Unset):
        servings (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferRecipeIdeasResponseDto]
    """

    kwargs = _get_kwargs(
        store_ids=store_ids,
        limit=limit,
        language=language,
        categories=categories,
        dietary_styles=dietary_styles,
        exclude_allergens=exclude_allergens,
        servings=servings,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    store_ids: list[str] | Unset = UNSET,
    limit: float | Unset = UNSET,
    language: str | Unset = UNSET,
    categories: list[OfferRecipeIdeasControllerFindCategoriesItem] | Unset = UNSET,
    dietary_styles: list[OfferRecipeIdeasControllerFindDietaryStylesItem] | Unset = UNSET,
    exclude_allergens: list[OfferRecipeIdeasControllerFindExcludeAllergensItem] | Unset = UNSET,
    servings: float | Unset = UNSET,
) -> OfferRecipeIdeasResponseDto | None:
    """Recipes whose ingredients are on offer at the caller’s markets

     Ranked by how much of the shopping list is covered right now. The recipes are AI-generated and
    permanently flagged as such; the prices are computed per request from the offers currently on the
    shelf, so they change rather than expire. An empty `ideas` array with `offeredIngredientCount: 0` is
    the "nothing useful this week" case, not an error.

    Args:
        store_ids (list[str] | Unset):
        limit (float | Unset):
        language (str | Unset):
        categories (list[OfferRecipeIdeasControllerFindCategoriesItem] | Unset):
        dietary_styles (list[OfferRecipeIdeasControllerFindDietaryStylesItem] | Unset):
        exclude_allergens (list[OfferRecipeIdeasControllerFindExcludeAllergensItem] | Unset):
        servings (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferRecipeIdeasResponseDto
    """

    return sync_detailed(
        client=client,
        store_ids=store_ids,
        limit=limit,
        language=language,
        categories=categories,
        dietary_styles=dietary_styles,
        exclude_allergens=exclude_allergens,
        servings=servings,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    store_ids: list[str] | Unset = UNSET,
    limit: float | Unset = UNSET,
    language: str | Unset = UNSET,
    categories: list[OfferRecipeIdeasControllerFindCategoriesItem] | Unset = UNSET,
    dietary_styles: list[OfferRecipeIdeasControllerFindDietaryStylesItem] | Unset = UNSET,
    exclude_allergens: list[OfferRecipeIdeasControllerFindExcludeAllergensItem] | Unset = UNSET,
    servings: float | Unset = UNSET,
) -> Response[OfferRecipeIdeasResponseDto]:
    """Recipes whose ingredients are on offer at the caller’s markets

     Ranked by how much of the shopping list is covered right now. The recipes are AI-generated and
    permanently flagged as such; the prices are computed per request from the offers currently on the
    shelf, so they change rather than expire. An empty `ideas` array with `offeredIngredientCount: 0` is
    the "nothing useful this week" case, not an error.

    Args:
        store_ids (list[str] | Unset):
        limit (float | Unset):
        language (str | Unset):
        categories (list[OfferRecipeIdeasControllerFindCategoriesItem] | Unset):
        dietary_styles (list[OfferRecipeIdeasControllerFindDietaryStylesItem] | Unset):
        exclude_allergens (list[OfferRecipeIdeasControllerFindExcludeAllergensItem] | Unset):
        servings (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OfferRecipeIdeasResponseDto]
    """

    kwargs = _get_kwargs(
        store_ids=store_ids,
        limit=limit,
        language=language,
        categories=categories,
        dietary_styles=dietary_styles,
        exclude_allergens=exclude_allergens,
        servings=servings,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    store_ids: list[str] | Unset = UNSET,
    limit: float | Unset = UNSET,
    language: str | Unset = UNSET,
    categories: list[OfferRecipeIdeasControllerFindCategoriesItem] | Unset = UNSET,
    dietary_styles: list[OfferRecipeIdeasControllerFindDietaryStylesItem] | Unset = UNSET,
    exclude_allergens: list[OfferRecipeIdeasControllerFindExcludeAllergensItem] | Unset = UNSET,
    servings: float | Unset = UNSET,
) -> OfferRecipeIdeasResponseDto | None:
    """Recipes whose ingredients are on offer at the caller’s markets

     Ranked by how much of the shopping list is covered right now. The recipes are AI-generated and
    permanently flagged as such; the prices are computed per request from the offers currently on the
    shelf, so they change rather than expire. An empty `ideas` array with `offeredIngredientCount: 0` is
    the "nothing useful this week" case, not an error.

    Args:
        store_ids (list[str] | Unset):
        limit (float | Unset):
        language (str | Unset):
        categories (list[OfferRecipeIdeasControllerFindCategoriesItem] | Unset):
        dietary_styles (list[OfferRecipeIdeasControllerFindDietaryStylesItem] | Unset):
        exclude_allergens (list[OfferRecipeIdeasControllerFindExcludeAllergensItem] | Unset):
        servings (float | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OfferRecipeIdeasResponseDto
    """

    return (
        await asyncio_detailed(
            client=client,
            store_ids=store_ids,
            limit=limit,
            language=language,
            categories=categories,
            dietary_styles=dietary_styles,
            exclude_allergens=exclude_allergens,
            servings=servings,
        )
    ).parsed
