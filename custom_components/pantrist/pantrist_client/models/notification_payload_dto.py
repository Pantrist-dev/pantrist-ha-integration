from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="NotificationPayloadDto")


@_attrs_define
class NotificationPayloadDto:
    """
    Attributes:
        title (str):
        body (str):
        android_channel_id (str):
    """

    title: str
    body: str
    android_channel_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        title = self.title

        body = self.body

        android_channel_id = self.android_channel_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "body": body,
                "android_channel_id": android_channel_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        title = d.pop("title")

        body = d.pop("body")

        android_channel_id = d.pop("android_channel_id")

        notification_payload_dto = cls(
            title=title,
            body=body,
            android_channel_id=android_channel_id,
        )

        notification_payload_dto.additional_properties = d
        return notification_payload_dto

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
