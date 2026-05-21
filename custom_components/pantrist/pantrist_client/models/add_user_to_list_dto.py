from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.role import Role
from ..types import UNSET, Unset

T = TypeVar("T", bound="AddUserToListDto")


@_attrs_define
class AddUserToListDto:
    """
    Attributes:
        user_uid (str): UID of the user to add
        role (Role | Unset): Role to assign to the user
    """

    user_uid: str
    role: Role | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        user_uid = self.user_uid

        role: str | Unset = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "userUid": user_uid,
            }
        )
        if role is not UNSET:
            field_dict["role"] = role

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        user_uid = d.pop("userUid")

        _role = d.pop("role", UNSET)
        role: Role | Unset
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = Role(_role)

        add_user_to_list_dto = cls(
            user_uid=user_uid,
            role=role,
        )

        add_user_to_list_dto.additional_properties = d
        return add_user_to_list_dto

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
