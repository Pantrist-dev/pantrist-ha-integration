from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.client_log_entry_dto_level import ClientLogEntryDtoLevel
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.client_log_entry_dto_data import ClientLogEntryDtoData


T = TypeVar("T", bound="ClientLogEntryDto")


@_attrs_define
class ClientLogEntryDto:
    """
    Attributes:
        level (ClientLogEntryDtoLevel):
        message (str): The log message.
        timestamp (str): When the log line was produced on the client. Example: 2026-05-14T12:34:56.000Z.
        session_id (str | Unset): Stable UUID for the current tab/PWA session.
        url (str | Unset): window.location.href at log time.
        user_agent (str | Unset):
        app_version (str | Unset): App build / version identifier.
        stack (str | Unset): Truncated stack trace.
        data (ClientLogEntryDtoData | Unset): Optional structured payload. PII MUST NOT be included here — these fields
            land in Loki for 7 days. Reviewed during implementation.
    """

    level: ClientLogEntryDtoLevel
    message: str
    timestamp: str
    session_id: str | Unset = UNSET
    url: str | Unset = UNSET
    user_agent: str | Unset = UNSET
    app_version: str | Unset = UNSET
    stack: str | Unset = UNSET
    data: ClientLogEntryDtoData | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        level = self.level.value

        message = self.message

        timestamp = self.timestamp

        session_id = self.session_id

        url = self.url

        user_agent = self.user_agent

        app_version = self.app_version

        stack = self.stack

        data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "level": level,
                "message": message,
                "timestamp": timestamp,
            }
        )
        if session_id is not UNSET:
            field_dict["sessionId"] = session_id
        if url is not UNSET:
            field_dict["url"] = url
        if user_agent is not UNSET:
            field_dict["userAgent"] = user_agent
        if app_version is not UNSET:
            field_dict["appVersion"] = app_version
        if stack is not UNSET:
            field_dict["stack"] = stack
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.client_log_entry_dto_data import ClientLogEntryDtoData

        d = dict(src_dict)
        level = ClientLogEntryDtoLevel(d.pop("level"))

        message = d.pop("message")

        timestamp = d.pop("timestamp")

        session_id = d.pop("sessionId", UNSET)

        url = d.pop("url", UNSET)

        user_agent = d.pop("userAgent", UNSET)

        app_version = d.pop("appVersion", UNSET)

        stack = d.pop("stack", UNSET)

        _data = d.pop("data", UNSET)
        data: ClientLogEntryDtoData | Unset
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = ClientLogEntryDtoData.from_dict(_data)

        client_log_entry_dto = cls(
            level=level,
            message=message,
            timestamp=timestamp,
            session_id=session_id,
            url=url,
            user_agent=user_agent,
            app_version=app_version,
            stack=stack,
            data=data,
        )

        client_log_entry_dto.additional_properties = d
        return client_log_entry_dto

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
