from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="NotificationSettingsDto")


@_attrs_define
class NotificationSettingsDto:
    """
    Attributes:
        notification_time (str | Unset):
        thirty_days (bool | Unset):
        seven_days (bool | Unset):
        at_expiry_date (bool | Unset):
    """

    notification_time: str | Unset = UNSET
    thirty_days: bool | Unset = UNSET
    seven_days: bool | Unset = UNSET
    at_expiry_date: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        notification_time = self.notification_time

        thirty_days = self.thirty_days

        seven_days = self.seven_days

        at_expiry_date = self.at_expiry_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if notification_time is not UNSET:
            field_dict["notificationTime"] = notification_time
        if thirty_days is not UNSET:
            field_dict["thirtyDays"] = thirty_days
        if seven_days is not UNSET:
            field_dict["sevenDays"] = seven_days
        if at_expiry_date is not UNSET:
            field_dict["atExpiryDate"] = at_expiry_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        notification_time = d.pop("notificationTime", UNSET)

        thirty_days = d.pop("thirtyDays", UNSET)

        seven_days = d.pop("sevenDays", UNSET)

        at_expiry_date = d.pop("atExpiryDate", UNSET)

        notification_settings_dto = cls(
            notification_time=notification_time,
            thirty_days=thirty_days,
            seven_days=seven_days,
            at_expiry_date=at_expiry_date,
        )

        notification_settings_dto.additional_properties = d
        return notification_settings_dto

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
