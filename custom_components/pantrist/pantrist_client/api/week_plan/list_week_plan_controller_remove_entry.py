from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.list_week_plan_controller_remove_entry_type import ListWeekPlanControllerRemoveEntryType
from ...models.week_plan_day_dto import WeekPlanDayDto
from ...types import UNSET, Response, Unset


def _get_kwargs(
    list_id: str,
    date: str,
    *,
    type_: ListWeekPlanControllerRemoveEntryType,
    uuid: str | Unset = UNSET,
    name: str | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_socket_id, Unset):
        headers["x-socket-id"] = x_socket_id

    params: dict[str, Any] = {}

    json_type_ = type_.value
    params["type"] = json_type_

    params["uuid"] = uuid

    params["name"] = name

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/list/{list_id}/weekPlan/{date}/entries".format(
            list_id=quote(str(list_id), safe=""),
            date=quote(str(date), safe=""),
        ),
        "params": params,
    }

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> WeekPlanDayDto | None:
    if response.status_code == 200:
        response_200 = WeekPlanDayDto.from_dict(response.json())

        return response_200

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
    type_: ListWeekPlanControllerRemoveEntryType,
    uuid: str | Unset = UNSET,
    name: str | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> Response[WeekPlanDayDto]:
    """Remove one entry from a day and keep the others

     Removes the recipe `uuid` (type recipe) or the manual entry `name` (type manual). Removing an entry
    the day does not hold changes nothing. Returns the whole day.

    Args:
        list_id (str):
        date (str):
        type_ (ListWeekPlanControllerRemoveEntryType):
        uuid (str | Unset):
        name (str | Unset):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WeekPlanDayDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        date=date,
        type_=type_,
        uuid=uuid,
        name=name,
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
    type_: ListWeekPlanControllerRemoveEntryType,
    uuid: str | Unset = UNSET,
    name: str | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> WeekPlanDayDto | None:
    """Remove one entry from a day and keep the others

     Removes the recipe `uuid` (type recipe) or the manual entry `name` (type manual). Removing an entry
    the day does not hold changes nothing. Returns the whole day.

    Args:
        list_id (str):
        date (str):
        type_ (ListWeekPlanControllerRemoveEntryType):
        uuid (str | Unset):
        name (str | Unset):
        x_socket_id (str | Unset):

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
        type_=type_,
        uuid=uuid,
        name=name,
        x_socket_id=x_socket_id,
    ).parsed


async def asyncio_detailed(
    list_id: str,
    date: str,
    *,
    client: AuthenticatedClient,
    type_: ListWeekPlanControllerRemoveEntryType,
    uuid: str | Unset = UNSET,
    name: str | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> Response[WeekPlanDayDto]:
    """Remove one entry from a day and keep the others

     Removes the recipe `uuid` (type recipe) or the manual entry `name` (type manual). Removing an entry
    the day does not hold changes nothing. Returns the whole day.

    Args:
        list_id (str):
        date (str):
        type_ (ListWeekPlanControllerRemoveEntryType):
        uuid (str | Unset):
        name (str | Unset):
        x_socket_id (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[WeekPlanDayDto]
    """

    kwargs = _get_kwargs(
        list_id=list_id,
        date=date,
        type_=type_,
        uuid=uuid,
        name=name,
        x_socket_id=x_socket_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    list_id: str,
    date: str,
    *,
    client: AuthenticatedClient,
    type_: ListWeekPlanControllerRemoveEntryType,
    uuid: str | Unset = UNSET,
    name: str | Unset = UNSET,
    x_socket_id: str | Unset = UNSET,
) -> WeekPlanDayDto | None:
    """Remove one entry from a day and keep the others

     Removes the recipe `uuid` (type recipe) or the manual entry `name` (type manual). Removing an entry
    the day does not hold changes nothing. Returns the whole day.

    Args:
        list_id (str):
        date (str):
        type_ (ListWeekPlanControllerRemoveEntryType):
        uuid (str | Unset):
        name (str | Unset):
        x_socket_id (str | Unset):

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
            type_=type_,
            uuid=uuid,
            name=name,
            x_socket_id=x_socket_id,
        )
    ).parsed
