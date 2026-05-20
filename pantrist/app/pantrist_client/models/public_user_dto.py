from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.public_user_dto_forced_premium_tariff import PublicUserDtoForcedPremiumTariff
from ..types import UNSET, Unset

T = TypeVar("T", bound="PublicUserDto")


@_attrs_define
class PublicUserDto:
    """
    Attributes:
        uid (str):
        display_name (str):
        forced_premium_tariff (PublicUserDtoForcedPremiumTariff | Unset):
    """

    uid: str
    display_name: str
    forced_premium_tariff: PublicUserDtoForcedPremiumTariff | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uid = self.uid

        display_name = self.display_name

        forced_premium_tariff: str | Unset = UNSET
        if not isinstance(self.forced_premium_tariff, Unset):
            forced_premium_tariff = self.forced_premium_tariff.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uid": uid,
                "displayName": display_name,
            }
        )
        if forced_premium_tariff is not UNSET:
            field_dict["forcedPremiumTariff"] = forced_premium_tariff

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uid = d.pop("uid")

        display_name = d.pop("displayName")

        _forced_premium_tariff = d.pop("forcedPremiumTariff", UNSET)
        forced_premium_tariff: PublicUserDtoForcedPremiumTariff | Unset
        if isinstance(_forced_premium_tariff, Unset):
            forced_premium_tariff = UNSET
        else:
            forced_premium_tariff = PublicUserDtoForcedPremiumTariff(_forced_premium_tariff)

        public_user_dto = cls(
            uid=uid,
            display_name=display_name,
            forced_premium_tariff=forced_premium_tariff,
        )

        public_user_dto.additional_properties = d
        return public_user_dto

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
