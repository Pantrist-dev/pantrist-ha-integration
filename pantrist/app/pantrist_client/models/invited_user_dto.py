from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="InvitedUserDto")


@_attrs_define
class InvitedUserDto:
    """
    Attributes:
        id (str):
        user_id (str):
        email (str):
        display_name (str):
        accepted (bool):
        created_at (datetime.datetime):
        updated_at (datetime.datetime):
    """

    id: str
    user_id: str
    email: str
    display_name: str
    accepted: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        user_id = self.user_id

        email = self.email

        display_name = self.display_name

        accepted = self.accepted

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "userId": user_id,
                "email": email,
                "displayName": display_name,
                "accepted": accepted,
                "createdAt": created_at,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        user_id = d.pop("userId")

        email = d.pop("email")

        display_name = d.pop("displayName")

        accepted = d.pop("accepted")

        created_at = isoparse(d.pop("createdAt"))

        updated_at = isoparse(d.pop("updatedAt"))

        invited_user_dto = cls(
            id=id,
            user_id=user_id,
            email=email,
            display_name=display_name,
            accepted=accepted,
            created_at=created_at,
            updated_at=updated_at,
        )

        invited_user_dto.additional_properties = d
        return invited_user_dto

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
