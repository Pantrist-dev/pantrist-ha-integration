from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.metric_equivalent_dto_unit import MetricEquivalentDtoUnit

T = TypeVar("T", bound="MetricEquivalentDto")


@_attrs_define
class MetricEquivalentDto:
    """
    Attributes:
        amount (float): The ingredient's whole amount expressed in the metric unit below Example: 250.
        unit (MetricEquivalentDtoUnit): Metric base unit: `g` for solids, `ml` for liquids Example: g.
    """

    amount: float
    unit: MetricEquivalentDtoUnit
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        unit = self.unit.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "unit": unit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount = d.pop("amount")

        unit = MetricEquivalentDtoUnit(d.pop("unit"))

        metric_equivalent_dto = cls(
            amount=amount,
            unit=unit,
        )

        metric_equivalent_dto.additional_properties = d
        return metric_equivalent_dto

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
