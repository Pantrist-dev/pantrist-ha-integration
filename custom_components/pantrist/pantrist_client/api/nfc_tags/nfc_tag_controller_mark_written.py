from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.nfc_tag_dto import NfcTagDto
from ...types import Response


def _get_kwargs(
    list_id: str,
    tag_id: str,
) -> dict[str, Any]:

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/list/{list_id}/nfc/tags/{tag_id}/written".format(
            list_id=quote(str(list_id), safe=""),
            tag_id=quote(str(tag_id), safe=""),
        ),
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> NfcTagDto | None:
    if response.status_code == 201:
        response_201 = NfcTagDto.from_dict(response.json())

        return response_201

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
) -> Response[NfcTagDto]:
    """Record that the tag was successfully written to a physical NFC tag

    Args:
        list_id (str):
        tag_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NfcTagDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        tag_id=tag_id,
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
) -> NfcTagDto | None:
    """Record that the tag was successfully written to a physical NFC tag

    Args:
        list_id (str):
        tag_id (str):

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
    ).parsed


async def asyncio_detailed(
    list_id: str,
    tag_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[NfcTagDto]:
    """Record that the tag was successfully written to a physical NFC tag

    Args:
        list_id (str):
        tag_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[NfcTagDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        tag_id=tag_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    tag_id: str,
    *,
    client: AuthenticatedClient,
) -> NfcTagDto | None:
    """Record that the tag was successfully written to a physical NFC tag

    Args:
        list_id (str):
        tag_id (str):

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
        )
    ).parsed
