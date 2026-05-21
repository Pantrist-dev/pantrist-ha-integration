from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.unit_dto import UnitDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    uid: str,
    *,
    body: UnitDto,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/list/{list_id}/units/{uid}".format(
            list_id=quote(str(list_id), safe=""),
            uid=quote(str(uid), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> UnitDto | None:
    if response.status_code == 200:
        response_200 = UnitDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[UnitDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    list_id: str,
    uid: str,
    *,
    client: AuthenticatedClient,
    body: UnitDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[UnitDto]:
    """Upsert a single unit

    Args:
        list_id (str):
        uid (str):
        x_socket_id (str | Unset):
        body (UnitDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UnitDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        uid=uid,
        body=body,
        x_socket_id=x_socket_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    uid: str,
    *,
    client: AuthenticatedClient,
    body: UnitDto,
    x_socket_id: str | Unset = UNSET,
) -> UnitDto | None:
    """Upsert a single unit

    Args:
        list_id (str):
        uid (str):
        x_socket_id (str | Unset):
        body (UnitDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UnitDto
    """

    return sync_detailed(
        list_id=list_id,
        uid=uid,
        client=client,
        body=body,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    uid: str,
    *,
    client: AuthenticatedClient,
    body: UnitDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[UnitDto]:
    """Upsert a single unit

    Args:
        list_id (str):
        uid (str):
        x_socket_id (str | Unset):
        body (UnitDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UnitDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        uid=uid,
        body=body,
        x_socket_id=x_socket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    uid: str,
    *,
    client: AuthenticatedClient,
    body: UnitDto,
    x_socket_id: str | Unset = UNSET,
) -> UnitDto | None:
    """Upsert a single unit

    Args:
        list_id (str):
        uid (str):
        x_socket_id (str | Unset):
        body (UnitDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UnitDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            uid=uid,
            client=client,
            body=body,
            x_socket_id=x_socket_id,
        )
    ).parsed
