from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.invited_user_dto import InvitedUserDto


T = TypeVar("T", bound="PremiumInvitationDto")


@_attrs_define
class PremiumInvitationDto:
    """
    Attributes:
        id (str):
        inviter_id (str):
        inviter_name (str):
        inviter_email (str):
        invited_users (list[InvitedUserDto]):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    inviter_id: str
    inviter_name: str
    inviter_email: str
    invited_users: list[InvitedUserDto]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        inviter_id = self.inviter_id

        inviter_name = self.inviter_name

        inviter_email = self.inviter_email

        invited_users = []
        for invited_users_item_data in self.invited_users:
            invited_users_item = invited_users_item_data.to_dict()
            invited_users.append(invited_users_item)

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "inviterId": inviter_id,
                "inviterName": inviter_name,
                "inviterEmail": inviter_email,
                "invitedUsers": invited_users,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.invited_user_dto import InvitedUserDto

        d = dict(src_dict)
        id = d.pop("id")

        inviter_id = d.pop("inviterId")

        inviter_name = d.pop("inviterName")

        inviter_email = d.pop("inviterEmail")

        invited_users = []
        _invited_users = d.pop("invitedUsers")
        for invited_users_item_data in _invited_users:
            invited_users_item = InvitedUserDto.from_dict(invited_users_item_data)

            invited_users.append(invited_users_item)

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        premium_invitation_dto = cls(
            id=id,
            inviter_id=inviter_id,
            inviter_name=inviter_name,
            inviter_email=inviter_email,
            invited_users=invited_users,
            created_at=created_at,
            updated_at=updated_at,
        )

        premium_invitation_dto.additional_properties = d
        return premium_invitation_dto

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
