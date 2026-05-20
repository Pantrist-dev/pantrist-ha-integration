from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_collection_assignment_dto import UpdateCollectionAssignmentDto
from ...types import Response


def _get_kwargs(
    recipe_uuid: str,
    *,
    body: UpdateCollectionAssignmentDto,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/recipe-collection/recipe/{recipe_uuid}".format(
            recipe_uuid=quote(str(recipe_uuid), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | None:
    if response.status_code == 200:
        return None

    if response.status_code == 401:
        return None

    if response.status_code == 404:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    recipe_uuid: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateCollectionAssignmentDto,
) -> Response[Any]:
    """Update recipe → collection assignments

     Replaces all collection assignments of a recipe with the provided collection UUIDs.

    Args:
        recipe_uuid (str):
        body (UpdateCollectionAssignmentDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        recipe_uuid=recipe_uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    recipe_uuid: str,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateCollectionAssignmentDto,
) -> Response[Any]:
    """Update recipe → collection assignments

     Replaces all collection assignments of a recipe with the provided collection UUIDs.

    Args:
        recipe_uuid (str):
        body (UpdateCollectionAssignmentDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        recipe_uuid=recipe_uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
