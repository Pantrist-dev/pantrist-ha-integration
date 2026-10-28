from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.role import Role
from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateInviteDto")


@_attrs_define
class CreateInviteDto:
    """
    Attributes:
        role (Role): Role to assign to the user
        ttl_minutes (float | Unset): How many minutes the invite stays valid for. Defaults to 60.
        recipient_uid (str | Unset): Pantrist user to send the invite to as a push notification, for inviting someone by
            e-mail address. Without it the invite is only a share link.
    """

    role: Role
    ttl_minutes: float | Unset = UNSET
    recipient_uid: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        role = self.role.value

        ttl_minutes = self.ttl_minutes

        recipient_uid = self.recipient_uid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "role": role,
            }
        )
        if ttl_minutes is not UNSET:
            field_dict["ttlMinutes"] = ttl_minutes
        if recipient_uid is not UNSET:
            field_dict["recipientUid"] = recipient_uid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        role = Role(d.pop("role"))

        ttl_minutes = d.pop("ttlMinutes", UNSET)

        recipient_uid = d.pop("recipientUid", UNSET)

        create_invite_dto = cls(
            role=role,
            ttl_minutes=ttl_minutes,
            recipient_uid=recipient_uid,
        )

        create_invite_dto.additional_properties = d
        return create_invite_dto

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
