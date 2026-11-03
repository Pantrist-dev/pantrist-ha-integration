from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.cook_recipe_reservation_dto import CookRecipeReservationDto
from ...models.cooked_recipe_reservation_dto import CookedRecipeReservationDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    recipe_uuid: str,
    *,
    body: CookRecipeReservationDto | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/list/{list_id}/pantryList/reservations/{recipe_uuid}/cooked".format(
            list_id=quote(str(list_id), safe=""),
            recipe_uuid=quote(str(recipe_uuid), safe=""),
        ),
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> CookedRecipeReservationDto | None:
    if response.status_code == 200:
        response_200 = CookedRecipeReservationDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CookedRecipeReservationDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    list_id: str,
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    body: CookRecipeReservationDto | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> Response[CookedRecipeReservationDto]:
    """Book a cooked recipe out of the pantry

     Books every reservation of the recipe out of its item, the way the app does: open packages first,
    then whole ones, and a remainder leaves a package open. The reservations are removed. `unbooked`
    lists reserved content the stock could not cover.

    Args:
        list_id (str):
        recipe_uuid (str):
        x_socket_id (str | Unset):
        body (CookRecipeReservationDto | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CookedRecipeReservationDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
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
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    body: CookRecipeReservationDto | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> CookedRecipeReservationDto | None:
    """Book a cooked recipe out of the pantry

     Books every reservation of the recipe out of its item, the way the app does: open packages first,
    then whole ones, and a remainder leaves a package open. The reservations are removed. `unbooked`
    lists reserved content the stock could not cover.

    Args:
        list_id (str):
        recipe_uuid (str):
        x_socket_id (str | Unset):
        body (CookRecipeReservationDto | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CookedRecipeReservationDto
    """

    return sync_detailed(
        list_id=list_id,
        recipe_uuid=recipe_uuid,
        client=client,
        body=body,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    body: CookRecipeReservationDto | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> Response[CookedRecipeReservationDto]:
    """Book a cooked recipe out of the pantry

     Books every reservation of the recipe out of its item, the way the app does: open packages first,
    then whole ones, and a remainder leaves a package open. The reservations are removed. `unbooked`
    lists reserved content the stock could not cover.

    Args:
        list_id (str):
        recipe_uuid (str):
        x_socket_id (str | Unset):
        body (CookRecipeReservationDto | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CookedRecipeReservationDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        recipe_uuid=recipe_uuid,
        body=body,
        x_socket_id=x_socket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    recipe_uuid: str,
    *,
    client: AuthenticatedClient,
    body: CookRecipeReservationDto | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> CookedRecipeReservationDto | None:
    """Book a cooked recipe out of the pantry

     Books every reservation of the recipe out of its item, the way the app does: open packages first,
    then whole ones, and a remainder leaves a package open. The reservations are removed. `unbooked`
    lists reserved content the stock could not cover.

    Args:
        list_id (str):
        recipe_uuid (str):
        x_socket_id (str | Unset):
        body (CookRecipeReservationDto | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CookedRecipeReservationDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            recipe_uuid=recipe_uuid,
            client=client,
            body=body,
            x_socket_id=x_socket_id,
        )
    ).parsed
