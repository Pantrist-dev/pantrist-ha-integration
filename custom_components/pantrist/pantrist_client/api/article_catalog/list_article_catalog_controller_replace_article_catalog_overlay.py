from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.article_catalog_overlay_dto import ArticleCatalogOverlayDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    *,
    body: ArticleCatalogOverlayDto,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/list/{list_id}/articleCatalog/overlay".format(
            list_id=quote(str(list_id), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | ArticleCatalogOverlayDto | None:
    if response.status_code == 200:
        response_200 = ArticleCatalogOverlayDto.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | ArticleCatalogOverlayDto]:
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
    body: ArticleCatalogOverlayDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[Any | ArticleCatalogOverlayDto]:
    """Replace a list's catalog with an overlay on the default catalog

     Stores exactly `rows` on the default catalog of `seedLang` and puts the list on the overlay.
    `seedLang` `none`: no default catalog, the rows are the whole catalog and none may be a tombstone.
    409 `CATALOG_OVERLAY_UNAVAILABLE`: the list is kept legacy, replace it with `PUT
    :listId/articleCatalog` instead. 400 `CATALOG_SEED_LANGUAGE_UNKNOWN` / `CATALOG_TOMBSTONE_NOT_SEED`
    for an unknown language or a tombstone without a `seed:` uuid (or any tombstone on `none`).

    Args:
        list_id (str):
        x_socket_id (str | Unset):
        body (ArticleCatalogOverlayDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ArticleCatalogOverlayDto]
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
    body: ArticleCatalogOverlayDto,
    x_socket_id: str | Unset = UNSET,
) -> Any | ArticleCatalogOverlayDto | None:
    """Replace a list's catalog with an overlay on the default catalog

     Stores exactly `rows` on the default catalog of `seedLang` and puts the list on the overlay.
    `seedLang` `none`: no default catalog, the rows are the whole catalog and none may be a tombstone.
    409 `CATALOG_OVERLAY_UNAVAILABLE`: the list is kept legacy, replace it with `PUT
    :listId/articleCatalog` instead. 400 `CATALOG_SEED_LANGUAGE_UNKNOWN` / `CATALOG_TOMBSTONE_NOT_SEED`
    for an unknown language or a tombstone without a `seed:` uuid (or any tombstone on `none`).

    Args:
        list_id (str):
        x_socket_id (str | Unset):
        body (ArticleCatalogOverlayDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ArticleCatalogOverlayDto
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
    body: ArticleCatalogOverlayDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[Any | ArticleCatalogOverlayDto]:
    """Replace a list's catalog with an overlay on the default catalog

     Stores exactly `rows` on the default catalog of `seedLang` and puts the list on the overlay.
    `seedLang` `none`: no default catalog, the rows are the whole catalog and none may be a tombstone.
    409 `CATALOG_OVERLAY_UNAVAILABLE`: the list is kept legacy, replace it with `PUT
    :listId/articleCatalog` instead. 400 `CATALOG_SEED_LANGUAGE_UNKNOWN` / `CATALOG_TOMBSTONE_NOT_SEED`
    for an unknown language or a tombstone without a `seed:` uuid (or any tombstone on `none`).

    Args:
        list_id (str):
        x_socket_id (str | Unset):
        body (ArticleCatalogOverlayDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ArticleCatalogOverlayDto]
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
    body: ArticleCatalogOverlayDto,
    x_socket_id: str | Unset = UNSET,
) -> Any | ArticleCatalogOverlayDto | None:
    """Replace a list's catalog with an overlay on the default catalog

     Stores exactly `rows` on the default catalog of `seedLang` and puts the list on the overlay.
    `seedLang` `none`: no default catalog, the rows are the whole catalog and none may be a tombstone.
    409 `CATALOG_OVERLAY_UNAVAILABLE`: the list is kept legacy, replace it with `PUT
    :listId/articleCatalog` instead. 400 `CATALOG_SEED_LANGUAGE_UNKNOWN` / `CATALOG_TOMBSTONE_NOT_SEED`
    for an unknown language or a tombstone without a `seed:` uuid (or any tombstone on `none`).

    Args:
        list_id (str):
        x_socket_id (str | Unset):
        body (ArticleCatalogOverlayDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ArticleCatalogOverlayDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            client=client,
            body=body,
            x_socket_id=x_socket_id,
        )
    ).parsed
