from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.notification_payload_dto import NotificationPayloadDto
    from ..models.send_notification_dto_data import SendNotificationDtoData


T = TypeVar("T", bound="SendNotificationDto")


@_attrs_define
class SendNotificationDto:
    """
    Attributes:
        topic (str):
        notification (NotificationPayloadDto):
        data (SendNotificationDtoData | Unset):
    """

    topic: str
    notification: NotificationPayloadDto
    data: SendNotificationDtoData | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        topic = self.topic

        notification = self.notification.to_dict()

        data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "topic": topic,
                "notification": notification,
            }
        )
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.notification_payload_dto import NotificationPayloadDto
        from ..models.send_notification_dto_data import SendNotificationDtoData

        d = dict(src_dict)
        topic = d.pop("topic")

        notification = NotificationPayloadDto.from_dict(d.pop("notification"))

        _data = d.pop("data", UNSET)
        data: SendNotificationDtoData | Unset
        if isinstance(_data, Unset) or _data is None:
            data = UNSET
        else:
            data = SendNotificationDtoData.from_dict(_data)

        send_notification_dto = cls(
            topic=topic,
            notification=notification,
            data=data,
        )

        send_notification_dto.additional_properties = d
        return send_notification_dto

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
