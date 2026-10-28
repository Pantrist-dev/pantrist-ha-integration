from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangeEmailDto")


@_attrs_define
class ChangeEmailDto:
    """
    Attributes:
        new_email (str):
        current_password (str | Unset): Required when the account has a password.
    """

    new_email: str
    current_password: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        new_email = self.new_email

        current_password = self.current_password

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "newEmail": new_email,
            }
        )
        if current_password is not UNSET:
            field_dict["currentPassword"] = current_password

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        new_email = d.pop("newEmail")

        current_password = d.pop("currentPassword", UNSET)

        change_email_dto = cls(
            new_email=new_email,
            current_password=current_password,
        )

        change_email_dto.additional_properties = d
        return change_email_dto

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
