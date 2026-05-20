from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_invite_dto import CreateInviteDto
from ...models.list_invite_dto import ListInviteDto
from ...types import Response


def _get_kwargs(
    list_id: str,
    *,
    body: CreateInviteDto,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/list/{list_id}/invites".format(
            list_id=quote(str(list_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ListInviteDto | None:
    if response.status_code == 201:
        response_201 = ListInviteDto.from_dict(response.json())

        return response_201

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ListInviteDto]:
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
    body: CreateInviteDto,
) -> Response[ListInviteDto]:
    """Create a share-link invite for a list (owner only)

    Args:
        list_id (str):
        body (CreateInviteDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListInviteDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateInviteDto,
) -> ListInviteDto | None:
    """Create a share-link invite for a list (owner only)

    Args:
        list_id (str):
        body (CreateInviteDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListInviteDto
    """

    return sync_detailed(
        list_id=list_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateInviteDto,
) -> Response[ListInviteDto]:
    """Create a share-link invite for a list (owner only)

    Args:
        list_id (str):
        body (CreateInviteDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListInviteDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    *,
    client: AuthenticatedClient,
    body: CreateInviteDto,
) -> ListInviteDto | None:
    """Create a share-link invite for a list (owner only)

    Args:
        list_id (str):
        body (CreateInviteDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListInviteDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            client=client,
            body=body,
        )
    ).parsed
