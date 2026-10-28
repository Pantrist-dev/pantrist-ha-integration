from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.market_arrival_transition_dto import MarketArrivalTransitionDto
from ...types import Response


def _get_kwargs(
    *,
    body: MarketArrivalTransitionDto,
    x_market_arrival_token: str,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["x-market-arrival-token"] = x_market_arrival_token

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/market-arrival/transition",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | None:
    if response.status_code == 204:
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
    *,
    client: AuthenticatedClient | Client,
    body: MarketArrivalTransitionDto,
    x_market_arrival_token: str,
) -> Response[Any]:
    """Report a geofence transition (native only)

    Args:
        x_market_arrival_token (str):
        body (MarketArrivalTransitionDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
        x_market_arrival_token=x_market_arrival_token,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: MarketArrivalTransitionDto,
    x_market_arrival_token: str,
) -> Response[Any]:
    """Report a geofence transition (native only)

    Args:
        x_market_arrival_token (str):
        body (MarketArrivalTransitionDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        body=body,
        x_market_arrival_token=x_market_arrival_token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
