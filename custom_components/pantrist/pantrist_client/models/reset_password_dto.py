from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResetPasswordDto")


@_attrs_define
class ResetPasswordDto:
    """
    Attributes:
        token (str): Token from the reset link.
        new_password (str):
        client (str | Unset): Client label: ios, android, web, wear, …
        device_name (str | Unset): Human readable device name for the session list.
    """

    token: str
    new_password: str
    client: str | Unset = UNSET
    device_name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token = self.token

        new_password = self.new_password

        client = self.client

        device_name = self.device_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token": token,
                "newPassword": new_password,
            }
        )
        if client is not UNSET:
            field_dict["client"] = client
        if device_name is not UNSET:
            field_dict["deviceName"] = device_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        token = d.pop("token")

        new_password = d.pop("newPassword")

        client = d.pop("client", UNSET)

        device_name = d.pop("deviceName", UNSET)

        reset_password_dto = cls(
            token=token,
            new_password=new_password,
            client=client,
            device_name=device_name,
        )

        reset_password_dto.additional_properties = d
        return reset_password_dto

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
