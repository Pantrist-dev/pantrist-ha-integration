from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.nfc_tag_dto import NfcTagDto
from ...models.update_nfc_tag_dto import UpdateNfcTagDto
from ...types import Response


def _get_kwargs(
    list_id: str,
    tag_id: str,
    *,
    body: UpdateNfcTagDto,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/list/{list_id}/nfc/tags/{tag_id}".format(
            list_id=quote(str(list_id), safe=""),
            tag_id=quote(str(tag_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> NfcTagDto | None:
    if response.status_code == 200:
        response_200 = NfcTagDto.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[NfcTagDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    list_id: str,
    tag_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateNfcTagDto,
) -> Response[NfcTagDto]:
    """Update an NFC tag mapping

    Args:
        list_id (str):
        tag_id (str):
        body (UpdateNfcTagDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NfcTagDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        tag_id=tag_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    tag_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateNfcTagDto,
) -> NfcTagDto | None:
    """Update an NFC tag mapping

    Args:
        list_id (str):
        tag_id (str):
        body (UpdateNfcTagDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        NfcTagDto
    """

    return sync_detailed(
        list_id=list_id,
        tag_id=tag_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    tag_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateNfcTagDto,
) -> Response[NfcTagDto]:
    """Update an NFC tag mapping

    Args:
        list_id (str):
        tag_id (str):
        body (UpdateNfcTagDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NfcTagDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        tag_id=tag_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    tag_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateNfcTagDto,
) -> NfcTagDto | None:
    """Update an NFC tag mapping

    Args:
        list_id (str):
        tag_id (str):
        body (UpdateNfcTagDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        NfcTagDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            tag_id=tag_id,
            client=client,
            body=body,
        )
    ).parsed
