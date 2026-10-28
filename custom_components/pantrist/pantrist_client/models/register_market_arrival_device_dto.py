from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RegisterMarketArrivalDeviceDto")


@_attrs_define
class RegisterMarketArrivalDeviceDto:
    """
    Attributes:
        fcm_token (str | Unset): This phone's FCM token, so the arrival push reaches only it. Without one the push goes
            to all of the user's devices.
    """

    fcm_token: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        fcm_token = self.fcm_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fcm_token is not UNSET:
            field_dict["fcmToken"] = fcm_token

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        fcm_token = d.pop("fcmToken", UNSET)

        register_market_arrival_device_dto = cls(
            fcm_token=fcm_token,
        )

        register_market_arrival_device_dto.additional_properties = d
        return register_market_arrival_device_dto

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
