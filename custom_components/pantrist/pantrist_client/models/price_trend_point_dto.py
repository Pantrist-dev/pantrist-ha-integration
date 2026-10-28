from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PriceTrendPointDto")


@_attrs_define
class PriceTrendPointDto:
    """
    Attributes:
        date (str): Purchase date (ISO string).
        unit_price (float): Price of one unit (package) of the purchase.
        content_volume (float):
        unit_id (str):
        price_per_content (float | Unset): Unit price divided by the content volume, when known.
    """

    date: str
    unit_price: float
    content_volume: float
    unit_id: str
    price_per_content: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        unit_price = self.unit_price

        content_volume = self.content_volume

        unit_id = self.unit_id

        price_per_content = self.price_per_content

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "unitPrice": unit_price,
                "contentVolume": content_volume,
                "unitId": unit_id,
            }
        )
        if price_per_content is not UNSET:
            field_dict["pricePerContent"] = price_per_content

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        date = d.pop("date")

        unit_price = d.pop("unitPrice")

        content_volume = d.pop("contentVolume")

        unit_id = d.pop("unitId")

        price_per_content = d.pop("pricePerContent", UNSET)

        price_trend_point_dto = cls(
            date=date,
            unit_price=unit_price,
            content_volume=content_volume,
            unit_id=unit_id,
            price_per_content=price_per_content,
        )

        price_trend_point_dto.additional_properties = d
        return price_trend_point_dto

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
