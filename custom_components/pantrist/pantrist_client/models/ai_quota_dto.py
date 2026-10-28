from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="AiQuotaDto")


@_attrs_define
class AiQuotaDto:
    """
    Attributes:
        unlimited (bool): Premium: AI features without a monthly limit.
        limit (float): AI features a free account gets per month.
        used (float): AI features used this month.
        remaining (float): AI features left this month; 0 when unlimited.
    """

    unlimited: bool
    limit: float
    used: float
    remaining: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        unlimited = self.unlimited

        limit = self.limit

        used = self.used

        remaining = self.remaining

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "unlimited": unlimited,
                "limit": limit,
                "used": used,
                "remaining": remaining,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        unlimited = d.pop("unlimited")

        limit = d.pop("limit")

        used = d.pop("used")

        remaining = d.pop("remaining")

        ai_quota_dto = cls(
            unlimited=unlimited,
            limit=limit,
            used=used,
            remaining=remaining,
        )

        ai_quota_dto.additional_properties = d
        return ai_quota_dto

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
