from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.catalog_mapping_entry_dto import CatalogMappingEntryDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    receipt_name: str,
    *,
    body: CatalogMappingEntryDto,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/list/{list_id}/catalogToReceiptNameMapping/{receipt_name}".format(
            list_id=quote(str(list_id), safe=""),
            receipt_name=quote(str(receipt_name), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CatalogMappingEntryDto | None:
    if response.status_code == 200:
        response_200 = CatalogMappingEntryDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[CatalogMappingEntryDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    list_id: str,
    receipt_name: str,
    *,
    client: AuthenticatedClient,
    body: CatalogMappingEntryDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[CatalogMappingEntryDto]:
    """Upsert a single receipt name mapping

    Args:
        list_id (str):
        receipt_name (str):
        x_socket_id (str | Unset):
        body (CatalogMappingEntryDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CatalogMappingEntryDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        receipt_name=receipt_name,
        body=body,
        x_socket_id=x_socket_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    receipt_name: str,
    *,
    client: AuthenticatedClient,
    body: CatalogMappingEntryDto,
    x_socket_id: str | Unset = UNSET,
) -> CatalogMappingEntryDto | None:
    """Upsert a single receipt name mapping

    Args:
        list_id (str):
        receipt_name (str):
        x_socket_id (str | Unset):
        body (CatalogMappingEntryDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CatalogMappingEntryDto
    """

    return sync_detailed(
        list_id=list_id,
        receipt_name=receipt_name,
        client=client,
        body=body,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    receipt_name: str,
    *,
    client: AuthenticatedClient,
    body: CatalogMappingEntryDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[CatalogMappingEntryDto]:
    """Upsert a single receipt name mapping

    Args:
        list_id (str):
        receipt_name (str):
        x_socket_id (str | Unset):
        body (CatalogMappingEntryDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CatalogMappingEntryDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        receipt_name=receipt_name,
        body=body,
        x_socket_id=x_socket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    receipt_name: str,
    *,
    client: AuthenticatedClient,
    body: CatalogMappingEntryDto,
    x_socket_id: str | Unset = UNSET,
) -> CatalogMappingEntryDto | None:
    """Upsert a single receipt name mapping

    Args:
        list_id (str):
        receipt_name (str):
        x_socket_id (str | Unset):
        body (CatalogMappingEntryDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CatalogMappingEntryDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            receipt_name=receipt_name,
            client=client,
            body=body,
            x_socket_id=x_socket_id,
        )
    ).parsed
