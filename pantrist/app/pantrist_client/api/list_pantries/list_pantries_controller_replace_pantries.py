from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.pantry_location_dto import PantryLocationDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    *,
    body: list[PantryLocationDto],
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/list/{list_id}/pantries".format(
            list_id=quote(str(list_id), safe=""),
        ),
    }

    _kwargs["json"] = []
    for body_item_data in body:
        body_item = body_item_data.to_dict()
        _kwargs["json"].append(body_item)

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> list[PantryLocationDto] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PantryLocationDto.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[PantryLocationDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    list_id: str,
    *,
    client: AuthenticatedClient,
    body: list[PantryLocationDto],
    x_socket_id: str | Unset = UNSET,
) -> Response[list[PantryLocationDto]]:
    """Replace all pantries (storage locations) for a list

    Args:
        list_id (str):
        x_socket_id (str | Unset):
        body (list[PantryLocationDto]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[PantryLocationDto]]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        body=body,
        x_socket_id=x_socket_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    *,
    client: AuthenticatedClient,
    body: list[PantryLocationDto],
    x_socket_id: str | Unset = UNSET,
) -> list[PantryLocationDto] | None:
    """Replace all pantries (storage locations) for a list

    Args:
        list_id (str):
        x_socket_id (str | Unset):
        body (list[PantryLocationDto]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[PantryLocationDto]
    """

    return sync_detailed(
        list_id=list_id,
        client=client,
        body=body,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    *,
    client: AuthenticatedClient,
    body: list[PantryLocationDto],
    x_socket_id: str | Unset = UNSET,
) -> Response[list[PantryLocationDto]]:
    """Replace all pantries (storage locations) for a list

    Args:
        list_id (str):
        x_socket_id (str | Unset):
        body (list[PantryLocationDto]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[PantryLocationDto]]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        body=body,
        x_socket_id=x_socket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    *,
    client: AuthenticatedClient,
    body: list[PantryLocationDto],
    x_socket_id: str | Unset = UNSET,
) -> list[PantryLocationDto] | None:
    """Replace all pantries (storage locations) for a list

    Args:
        list_id (str):
        x_socket_id (str | Unset):
        body (list[PantryLocationDto]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[PantryLocationDto]
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            client=client,
            body=body,
            x_socket_id=x_socket_id,
        )
    ).parsed
