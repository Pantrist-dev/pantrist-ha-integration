from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.week_plan_day_dto import WeekPlanDayDto
from ...models.week_plan_receipt_dto import WeekPlanReceiptDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    date: str,
    *,
    body: WeekPlanReceiptDto,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/list/{list_id}/weekPlan/{date}/entries".format(
            list_id=quote(str(list_id), safe=""),
            date=quote(str(date), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> WeekPlanDayDto | None:
    if response.status_code == 201:
        response_201 = WeekPlanDayDto.from_dict(response.json())

        return response_201

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[WeekPlanDayDto]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    list_id: str,
    date: str,
    *,
    client: AuthenticatedClient,
    body: WeekPlanReceiptDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[WeekPlanDayDto]:
    """Add one entry to a day and keep the others

     Unlike PUT, which replaces the whole day with what the caller has, this leaves entries the caller
    has not seen yet (planned on another device) alone. Adding an entry the day already holds changes
    nothing, so a retried request never plans a recipe twice. Returns the whole day.

    Args:
        list_id (str):
        date (str):
        x_socket_id (str | Unset):
        body (WeekPlanReceiptDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WeekPlanDayDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        date=date,
        body=body,
        x_socket_id=x_socket_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    list_id: str,
    date: str,
    *,
    client: AuthenticatedClient,
    body: WeekPlanReceiptDto,
    x_socket_id: str | Unset = UNSET,
) -> WeekPlanDayDto | None:
    """Add one entry to a day and keep the others

     Unlike PUT, which replaces the whole day with what the caller has, this leaves entries the caller
    has not seen yet (planned on another device) alone. Adding an entry the day already holds changes
    nothing, so a retried request never plans a recipe twice. Returns the whole day.

    Args:
        list_id (str):
        date (str):
        x_socket_id (str | Unset):
        body (WeekPlanReceiptDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WeekPlanDayDto
    """

    return sync_detailed(
        list_id=list_id,
        date=date,
        client=client,
        body=body,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    date: str,
    *,
    client: AuthenticatedClient,
    body: WeekPlanReceiptDto,
    x_socket_id: str | Unset = UNSET,
) -> Response[WeekPlanDayDto]:
    """Add one entry to a day and keep the others

     Unlike PUT, which replaces the whole day with what the caller has, this leaves entries the caller
    has not seen yet (planned on another device) alone. Adding an entry the day already holds changes
    nothing, so a retried request never plans a recipe twice. Returns the whole day.

    Args:
        list_id (str):
        date (str):
        x_socket_id (str | Unset):
        body (WeekPlanReceiptDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WeekPlanDayDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        date=date,
        body=body,
        x_socket_id=x_socket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    date: str,
    *,
    client: AuthenticatedClient,
    body: WeekPlanReceiptDto,
    x_socket_id: str | Unset = UNSET,
) -> WeekPlanDayDto | None:
    """Add one entry to a day and keep the others

     Unlike PUT, which replaces the whole day with what the caller has, this leaves entries the caller
    has not seen yet (planned on another device) alone. Adding an entry the day already holds changes
    nothing, so a retried request never plans a recipe twice. Returns the whole day.

    Args:
        list_id (str):
        date (str):
        x_socket_id (str | Unset):
        body (WeekPlanReceiptDto):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        WeekPlanDayDto
    """

    return (
        await asyncio_detailed(
            list_id=list_id,
            date=date,
            client=client,
            body=body,
            x_socket_id=x_socket_id,
        )
    ).parsed
