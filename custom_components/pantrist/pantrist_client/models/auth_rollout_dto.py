from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auth_rollout_dto_mode import AuthRolloutDtoMode
from ..types import UNSET, Unset

T = TypeVar("T", bound="AuthRolloutDto")


@_attrs_define
class AuthRolloutDto:
    """
    Attributes:
        mode (AuthRolloutDtoMode):
        enabled (bool): Whether the caller (identified by the bearer token, Firebase or Pantrist) may sign in through
            /auth. Without a token this reflects the global mode only.
        new_accounts (bool): Whether brand-new accounts may be created through /auth.
        migrated (bool | Unset): True when the caller already has a Pantrist credential (password or linked provider) or
            an active session, i.e. was migrated before. Only set when a token was sent.
    """

    mode: AuthRolloutDtoMode
    enabled: bool
    new_accounts: bool
    migrated: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.value

        enabled = self.enabled

        new_accounts = self.new_accounts

        migrated = self.migrated

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mode": mode,
                "enabled": enabled,
                "newAccounts": new_accounts,
            }
        )
        if migrated is not UNSET:
            field_dict["migrated"] = migrated

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = AuthRolloutDtoMode(d.pop("mode"))

        enabled = d.pop("enabled")

        new_accounts = d.pop("newAccounts")

        migrated = d.pop("migrated", UNSET)

        auth_rollout_dto = cls(
            mode=mode,
            enabled=enabled,
            new_accounts=new_accounts,
            migrated=migrated,
        )

        auth_rollout_dto.additional_properties = d
        return auth_rollout_dto

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
