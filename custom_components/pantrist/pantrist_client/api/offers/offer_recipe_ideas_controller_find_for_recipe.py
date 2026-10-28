from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offer_recipe_idea_dto import OfferRecipeIdeaDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    recipe_uuid: str,
    *,
    store_ids: list[str] | Unset = UNSET,
    language: str | Unset = UNSET,
    servings: float | Unset = UNSET,
    include_diet_filtered: bool | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    json_store_ids: list[str] | Unset = UNSET
    if not isinstance(store_ids, Unset):
        json_store_ids = store_ids

    params["storeIds"] = json_store_ids

    params["language"] = language

    params["servings"] = servings

    params["includeDietFiltered"] = include_diet_filtered

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/offers/recipe-ideas/{recipe_uuid}".format(
            recipe_uuid=quote(str(recipe_uuid), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | OfferRecipeIdeaDto | None:
    if response.status_code == 200:
        response_200 = OfferRecipeIdeaDto.from_dict(response.json())

        return response_200

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | OfferRecipeIdeaDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    store_ids: list[str] | Unset = UNSET,
    language: str | Unset = UNSET,
    servings: float | Unset = UNSET,
    include_diet_filtered: bool | Unset = UNSET,
) -> Response[Any | OfferRecipeIdeaDto]:
    """One recipe priced against the offers at the caller’s markets

     Every ingredient of the recipe with the offer currently covering it, if any, plus the same counts
    and cost estimate the recipe ideas carry. A recipe with nothing on offer is still returned, with
    `matchedIngredientCount: 0`; only a recipe the caller may not see is a 404.

    Args:
        recipe_uuid (str):
        store_ids (list[str] | Unset):
        language (str | Unset):
        servings (float | Unset):
        include_diet_filtered (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | OfferRecipeIdeaDto]
    """

    kwargs = _get_kwargs(
        recipe_uuid=recipe_uuid,
        store_ids=store_ids,
        language=language,
        servings=servings,
        include_diet_filtered=include_diet_filtered,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    store_ids: list[str] | Unset = UNSET,
    language: str | Unset = UNSET,
    servings: float | Unset = UNSET,
    include_diet_filtered: bool | Unset = UNSET,
) -> Any | OfferRecipeIdeaDto | None:
    """One recipe priced against the offers at the caller’s markets

     Every ingredient of the recipe with the offer currently covering it, if any, plus the same counts
    and cost estimate the recipe ideas carry. A recipe with nothing on offer is still returned, with
    `matchedIngredientCount: 0`; only a recipe the caller may not see is a 404.

    Args:
        recipe_uuid (str):
        store_ids (list[str] | Unset):
        language (str | Unset):
        servings (float | Unset):
        include_diet_filtered (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | OfferRecipeIdeaDto
    """

    return sync_detailed(
        recipe_uuid=recipe_uuid,
        client=client,
        store_ids=store_ids,
        language=language,
        servings=servings,
        include_diet_filtered=include_diet_filtered,
    ).parsed


async def asyncio_detailed(
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    store_ids: list[str] | Unset = UNSET,
    language: str | Unset = UNSET,
    servings: float | Unset = UNSET,
    include_diet_filtered: bool | Unset = UNSET,
) -> Response[Any | OfferRecipeIdeaDto]:
    """One recipe priced against the offers at the caller’s markets

     Every ingredient of the recipe with the offer currently covering it, if any, plus the same counts
    and cost estimate the recipe ideas carry. A recipe with nothing on offer is still returned, with
    `matchedIngredientCount: 0`; only a recipe the caller may not see is a 404.

    Args:
        recipe_uuid (str):
        store_ids (list[str] | Unset):
        language (str | Unset):
        servings (float | Unset):
        include_diet_filtered (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | OfferRecipeIdeaDto]
    """

    kwargs = _get_kwargs(
        recipe_uuid=recipe_uuid,
        store_ids=store_ids,
        language=language,
        servings=servings,
        include_diet_filtered=include_diet_filtered,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    store_ids: list[str] | Unset = UNSET,
    language: str | Unset = UNSET,
    servings: float | Unset = UNSET,
    include_diet_filtered: bool | Unset = UNSET,
) -> Any | OfferRecipeIdeaDto | None:
    """One recipe priced against the offers at the caller’s markets

     Every ingredient of the recipe with the offer currently covering it, if any, plus the same counts
    and cost estimate the recipe ideas carry. A recipe with nothing on offer is still returned, with
    `matchedIngredientCount: 0`; only a recipe the caller may not see is a 404.

    Args:
        recipe_uuid (str):
        store_ids (list[str] | Unset):
        language (str | Unset):
        servings (float | Unset):
        include_diet_filtered (bool | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | OfferRecipeIdeaDto
    """

    return (
        await asyncio_detailed(
            recipe_uuid=recipe_uuid,
            client=client,
            store_ids=store_ids,
            language=language,
            servings=servings,
            include_diet_filtered=include_diet_filtered,
        )
    ).parsed
