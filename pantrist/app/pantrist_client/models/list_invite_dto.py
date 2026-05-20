from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.role import Role
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListInviteDto")


@_attrs_define
class ListInviteDto:
    """
    Attributes:
        token (str): Opaque token embedded in the share link
        list_uuid (str): List the invite grants access to
        role (Role): Role to assign to the user
        created_by (str): UID of the owner who created the invite
        created_at (datetime.datetime): When the invite was created
        expires_at (datetime.datetime): When the invite stops being accepted
        revoked_at (datetime.datetime | None | Unset): When the invite was revoked, if it has been
    """

    token: str
    list_uuid: str
    role: Role
    created_by: str
    created_at: datetime.datetime
    expires_at: datetime.datetime
    revoked_at: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        token = self.token

        list_uuid = self.list_uuid

        role = self.role.value

        created_by = self.created_by

        created_at = self.created_at.isoformat()

        expires_at = self.expires_at.isoformat()

        revoked_at: None | str | Unset
        if isinstance(self.revoked_at, Unset):
            revoked_at = UNSET
        elif isinstance(self.revoked_at, datetime.datetime):
            revoked_at = self.revoked_at.isoformat()
        else:
            revoked_at = self.revoked_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "token": token,
                "listUuid": list_uuid,
                "role": role,
                "createdBy": created_by,
                "createdAt": created_at,
                "expiresAt": expires_at,
            }
        )
        if revoked_at is not UNSET:
            field_dict["revokedAt"] = revoked_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        token = d.pop("token")

        list_uuid = d.pop("listUuid")

        role = Role(d.pop("role"))

        created_by = d.pop("createdBy")

        created_at = isoparse(d.pop("createdAt"))

        expires_at = isoparse(d.pop("expiresAt"))

        def _parse_revoked_at(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                revoked_at_type_0 = isoparse(data)

                return revoked_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        revoked_at = _parse_revoked_at(d.pop("revokedAt", UNSET))

        list_invite_dto = cls(
            token=token,
            list_uuid=list_uuid,
            role=role,
            created_by=created_by,
            created_at=created_at,
            expires_at=expires_at,
            revoked_at=revoked_at,
        )

        list_invite_dto.additional_properties = d
        return list_invite_dto

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
