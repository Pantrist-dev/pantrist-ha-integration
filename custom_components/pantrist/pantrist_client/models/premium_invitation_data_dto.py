from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.premium_invitation_base_data_dto import PremiumInvitationBaseDataDto


T = TypeVar("T", bound="PremiumInvitationDataDto")


@_attrs_define
class PremiumInvitationDataDto:
    """
    Attributes:
        inviter_subscription_valid (bool | Unset):
        invitation (PremiumInvitationBaseDataDto | Unset):
        unaccepted_invitations (list[PremiumInvitationBaseDataDto] | Unset):
    """

    inviter_subscription_valid: bool | Unset = UNSET
    invitation: PremiumInvitationBaseDataDto | Unset = UNSET
    unaccepted_invitations: list[PremiumInvitationBaseDataDto] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        inviter_subscription_valid = self.inviter_subscription_valid

        invitation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.invitation, Unset):
            invitation = self.invitation.to_dict()

        unaccepted_invitations: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.unaccepted_invitations, Unset):
            unaccepted_invitations = []
            for unaccepted_invitations_item_data in self.unaccepted_invitations:
                unaccepted_invitations_item = unaccepted_invitations_item_data.to_dict()
                unaccepted_invitations.append(unaccepted_invitations_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if inviter_subscription_valid is not UNSET:
            field_dict["inviterSubscriptionValid"] = inviter_subscription_valid
        if invitation is not UNSET:
            field_dict["invitation"] = invitation
        if unaccepted_invitations is not UNSET:
            field_dict["unacceptedInvitations"] = unaccepted_invitations

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.premium_invitation_base_data_dto import PremiumInvitationBaseDataDto

        d = dict(src_dict)
        inviter_subscription_valid = d.pop("inviterSubscriptionValid", UNSET)

        _invitation = d.pop("invitation", UNSET)
        invitation: PremiumInvitationBaseDataDto | Unset
        if isinstance(_invitation, Unset):
            invitation = UNSET
        else:
            invitation = PremiumInvitationBaseDataDto.from_dict(_invitation)

        _unaccepted_invitations = d.pop("unacceptedInvitations", UNSET)
        unaccepted_invitations: list[PremiumInvitationBaseDataDto] | Unset = UNSET
        if _unaccepted_invitations is not UNSET:
            unaccepted_invitations = []
            for unaccepted_invitations_item_data in _unaccepted_invitations:
                unaccepted_invitations_item = PremiumInvitationBaseDataDto.from_dict(unaccepted_invitations_item_data)

                unaccepted_invitations.append(unaccepted_invitations_item)

        premium_invitation_data_dto = cls(
            inviter_subscription_valid=inviter_subscription_valid,
            invitation=invitation,
            unaccepted_invitations=unaccepted_invitations,
        )

        premium_invitation_data_dto.additional_properties = d
        return premium_invitation_data_dto

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
