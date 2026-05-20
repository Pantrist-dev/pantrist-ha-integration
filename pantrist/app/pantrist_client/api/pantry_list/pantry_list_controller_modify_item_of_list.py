from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.item_dto import ItemDto
from ...models.update_item_dto import UpdateItemDto
from ...types import Response


def _get_kwargs(
    list_id: str,
    item_id: str,
    *,
    body: UpdateItemDto,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/pantry-list/{list_id}/{item_id}".format(
            list_id=quote(str(list_id), safe=""),
            item_id=quote(str(item_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ItemDto | None:
    if response.status_code == 200:
        response_200 = ItemDto.from_dict(response.json())

        return response_200

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ItemDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    list_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateItemDto,
) -> Response[Any | ItemDto]:
    """Updates the item from the pantry list. Not that you can't update the amount here! Use the 'change-
    amount' endpoint for that.

    Args:
        list_id (str):
        item_id (str):
        body (UpdateItemDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ItemDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        item_id=item_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateItemDto,
) -> Any | ItemDto | None:
    """Updates the item from the pantry list. Not that you can't update the amount here! Use the 'change-
    amount' endpoint for that.

    Args:
        list_id (str):
        item_id (str):
        body (UpdateItemDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ItemDto
    """

    return sync_detailed(
        list_id=list_id,
        item_id=item_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateItemDto,
) -> Response[Any | ItemDto]:
    """Updates the item from the pantry list. Not that you can't update the amount here! Use the 'change-
    amount' endpoint for that.

    Args:
        list_id (str):
        item_id (str):
        body (UpdateItemDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ItemDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        item_id=item_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    item_id: str,
    *,
    client: AuthenticatedClient,
    body: UpdateItemDto,
) -> Any | ItemDto | None:
    """Updates the item from the pantry list. Not that you can't update the amount here! Use the 'change-
    amount' endpoint for that.

    Args:
        list_id (str):
        item_id (str):
        body (UpdateItemDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ItemDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            item_id=item_id,
            client=client,
            body=body,
        )
    ).parsed
