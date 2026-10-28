from http import HTTPStatus
from typing import Any

import httpx

from ...client import AuthenticatedClient, Client
from ...models.help_article_dto import HelpArticleDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    q: str,
    lang: str | Unset = UNSET,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["q"] = q

    params["lang"] = lang

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/help/search",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> list[HelpArticleDto]:
    response_default = []
    _response_default = response.json()
    for response_default_item_data in _response_default:
        response_default_item = HelpArticleDto.from_dict(response_default_item_data)

        response_default.append(response_default_item)

    return response_default


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[list[HelpArticleDto]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    q: str,
    lang: str | Unset = UNSET,
) -> Response[list[HelpArticleDto]]:
    """Help articles from pantrist.com that match a question

    Args:
        q (str):
        lang (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[HelpArticleDto]]
    """

    kwargs = _get_kwargs(
        q=q,
        lang=lang,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    q: str,
    lang: str | Unset = UNSET,
) -> list[HelpArticleDto] | None:
    """Help articles from pantrist.com that match a question

    Args:
        q (str):
        lang (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[HelpArticleDto]
    """

    return sync_detailed(
        client=client,
        q=q,
        lang=lang,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    q: str,
    lang: str | Unset = UNSET,
) -> Response[list[HelpArticleDto]]:
    """Help articles from pantrist.com that match a question

    Args:
        q (str):
        lang (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[HelpArticleDto]]
    """

    kwargs = _get_kwargs(
        q=q,
        lang=lang,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    q: str,
    lang: str | Unset = UNSET,
) -> list[HelpArticleDto] | None:
    """Help articles from pantrist.com that match a question

    Args:
        q (str):
        lang (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[HelpArticleDto]
    """

    return (
        await asyncio_detailed(
            client=client,
            q=q,
            lang=lang,
        )
    ).parsed
