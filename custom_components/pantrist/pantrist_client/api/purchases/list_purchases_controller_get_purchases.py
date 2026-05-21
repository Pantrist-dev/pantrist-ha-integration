from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_purchases_controller_get_purchases_response_200 import (
    ListPurchasesControllerGetPurchasesResponse200,
)
from ...types import UNSET, Response


def _get_kwargs(
    list_id: str,
    *,
    from_: str,
    to: str,
) -> dict[str, Any]:

    params: dict[str, Any] = {}

    params["from"] = from_

    params["to"] = to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/list/{list_id}/purchases".format(
            list_id=quote(str(list_id), safe=""),
        ),
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ListPurchasesControllerGetPurchasesResponse200 | None:
    if response.status_code == 200:
        response_200 = ListPurchasesControllerGetPurchasesResponse200.from_dict(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ListPurchasesControllerGetPurchasesResponse200]:
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
    from_: str,
    to: str,
) -> Response[ListPurchasesControllerGetPurchasesResponse200]:
    """Get all purchases for a list. Optionally filter by from/to ISO dates.

    Args:
        list_id (str):
        from_ (str):
        to (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListPurchasesControllerGetPurchasesResponse200]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        from_=from_,
        to=to,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    *,
    client: AuthenticatedClient,
    from_: str,
    to: str,
) -> ListPurchasesControllerGetPurchasesResponse200 | None:
    """Get all purchases for a list. Optionally filter by from/to ISO dates.

    Args:
        list_id (str):
        from_ (str):
        to (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListPurchasesControllerGetPurchasesResponse200
    """

    return sync_detailed(
        list_id=list_id,
        client=client,
        from_=from_,
        to=to,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    *,
    client: AuthenticatedClient,
    from_: str,
    to: str,
) -> Response[ListPurchasesControllerGetPurchasesResponse200]:
    """Get all purchases for a list. Optionally filter by from/to ISO dates.

    Args:
        list_id (str):
        from_ (str):
        to (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListPurchasesControllerGetPurchasesResponse200]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        from_=from_,
        to=to,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    *,
    client: AuthenticatedClient,
    from_: str,
    to: str,
) -> ListPurchasesControllerGetPurchasesResponse200 | None:
    """Get all purchases for a list. Optionally filter by from/to ISO dates.

    Args:
        list_id (str):
        from_ (str):
        to (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListPurchasesControllerGetPurchasesResponse200
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            client=client,
            from_=from_,
            to=to,
        )
    ).parsed
