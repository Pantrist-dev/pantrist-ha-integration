from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateInvitationDto")


@_attrs_define
class CreateInvitationDto:
    """
    Attributes:
        invited_user_email (str | Unset):
        invited_user_uid (str | Unset): Uid of a member of one of the inviter's lists; others are rejected with 403.
    """

    invited_user_email: str | Unset = UNSET
    invited_user_uid: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        invited_user_email = self.invited_user_email

        invited_user_uid = self.invited_user_uid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if invited_user_email is not UNSET:
            field_dict["invitedUserEmail"] = invited_user_email
        if invited_user_uid is not UNSET:
            field_dict["invitedUserUid"] = invited_user_uid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        invited_user_email = d.pop("invitedUserEmail", UNSET)

        invited_user_uid = d.pop("invitedUserUid", UNSET)

        create_invitation_dto = cls(
            invited_user_email=invited_user_email,
            invited_user_uid=invited_user_uid,
        )

        create_invitation_dto.additional_properties = d
        return create_invitation_dto

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
