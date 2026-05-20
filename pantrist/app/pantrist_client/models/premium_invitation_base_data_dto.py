from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="PremiumInvitationBaseDataDto")


@_attrs_define
class PremiumInvitationBaseDataDto:
    """
    Attributes:
        inviter_uid (str):
        inviter_name (str):
        invitation_id (str):
    """

    inviter_uid: str
    inviter_name: str
    invitation_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        inviter_uid = self.inviter_uid

        inviter_name = self.inviter_name

        invitation_id = self.invitation_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "inviterUid": inviter_uid,
                "inviterName": inviter_name,
                "invitationId": invitation_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        inviter_uid = d.pop("inviterUid")

        inviter_name = d.pop("inviterName")

        invitation_id = d.pop("invitationId")

        premium_invitation_base_data_dto = cls(
            inviter_uid=inviter_uid,
            inviter_name=inviter_name,
            invitation_id=invitation_id,
        )

        premium_invitation_base_data_dto.additional_properties = d
        return premium_invitation_base_data_dto

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
