from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PriceTrendContentChangeDto")


@_attrs_define
class PriceTrendContentChangeDto:
    """
    Attributes:
        date (str): ISO date string of the change.
        from_ (float):
        to (float):
        unit_id (str):
        market_uid (str | Unset):
    """

    date: str
    from_: float
    to: float
    unit_id: str
    market_uid: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        from_ = self.from_

        to = self.to

        unit_id = self.unit_id

        market_uid = self.market_uid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "from": from_,
                "to": to,
                "unitId": unit_id,
            }
        )
        if market_uid is not UNSET:
            field_dict["marketUid"] = market_uid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = d.pop("date")

        from_ = d.pop("from")

        to = d.pop("to")

        unit_id = d.pop("unitId")

        market_uid = d.pop("marketUid", UNSET)

        price_trend_content_change_dto = cls(
            date=date,
            from_=from_,
            to=to,
            unit_id=unit_id,
            market_uid=market_uid,
        )

        price_trend_content_change_dto.additional_properties = d
        return price_trend_content_change_dto

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
