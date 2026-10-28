from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.recipe_match_state_dto import RecipeMatchStateDto
from ...models.recipe_match_state_request_dto import RecipeMatchStateRequestDto
from ...types import Response


def _get_kwargs(
    *,
    body: RecipeMatchStateRequestDto,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/recipe/match-state",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list[RecipeMatchStateDto] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = RecipeMatchStateDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[RecipeMatchStateDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: RecipeMatchStateRequestDto,
) -> Response[list[RecipeMatchStateDto]]:
    """Score a batch of recipes against the caller pantry

     Returns matching_count / ingredient_count / missingIngredients per requested uuid. Lets the recipe
    overview and the detail page show have/missing badges without forcing a pantry-filtered list query:
    the app batches the uuids currently in view and pulls just the match summary for them. Capped at 50
    uuids per request. With a token the pantry is hydrated server-side from the caller lists; without
    one, pass the device's pantry in `ingredients`. Staples are scored from the recipe side either way,
    so they come back even for an empty pantry. Only recipes the caller may see are reported on.

    Args:
        body (RecipeMatchStateRequestDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[RecipeMatchStateDto]]
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
    body: RecipeMatchStateRequestDto,
) -> list[RecipeMatchStateDto] | None:
    """Score a batch of recipes against the caller pantry

     Returns matching_count / ingredient_count / missingIngredients per requested uuid. Lets the recipe
    overview and the detail page show have/missing badges without forcing a pantry-filtered list query:
    the app batches the uuids currently in view and pulls just the match summary for them. Capped at 50
    uuids per request. With a token the pantry is hydrated server-side from the caller lists; without
    one, pass the device's pantry in `ingredients`. Staples are scored from the recipe side either way,
    so they come back even for an empty pantry. Only recipes the caller may see are reported on.

    Args:
        body (RecipeMatchStateRequestDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[RecipeMatchStateDto]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: RecipeMatchStateRequestDto,
) -> Response[list[RecipeMatchStateDto]]:
    """Score a batch of recipes against the caller pantry

     Returns matching_count / ingredient_count / missingIngredients per requested uuid. Lets the recipe
    overview and the detail page show have/missing badges without forcing a pantry-filtered list query:
    the app batches the uuids currently in view and pulls just the match summary for them. Capped at 50
    uuids per request. With a token the pantry is hydrated server-side from the caller lists; without
    one, pass the device's pantry in `ingredients`. Staples are scored from the recipe side either way,
    so they come back even for an empty pantry. Only recipes the caller may see are reported on.

    Args:
        body (RecipeMatchStateRequestDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[RecipeMatchStateDto]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: RecipeMatchStateRequestDto,
) -> list[RecipeMatchStateDto] | None:
    """Score a batch of recipes against the caller pantry

     Returns matching_count / ingredient_count / missingIngredients per requested uuid. Lets the recipe
    overview and the detail page show have/missing badges without forcing a pantry-filtered list query:
    the app batches the uuids currently in view and pulls just the match summary for them. Capped at 50
    uuids per request. With a token the pantry is hydrated server-side from the caller lists; without
    one, pass the device's pantry in `ingredients`. Staples are scored from the recipe side either way,
    so they come back even for an empty pantry. Only recipes the caller may see are reported on.

    Args:
        body (RecipeMatchStateRequestDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[RecipeMatchStateDto]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
