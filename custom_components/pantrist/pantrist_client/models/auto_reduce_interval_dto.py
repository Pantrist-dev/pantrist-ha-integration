from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auto_reduce_interval_dto_mode import AutoReduceIntervalDtoMode
from ..models.auto_reduce_interval_dto_unit import AutoReduceIntervalDtoUnit

T = TypeVar("T", bound="AutoReduceIntervalDto")


@_attrs_define
class AutoReduceIntervalDto:
    """
    Attributes:
        mode (AutoReduceIntervalDtoMode):
        amount (float): Quantity reduced per `unit`
        unit (AutoReduceIntervalDtoUnit):
    """

    mode: AutoReduceIntervalDtoMode
    amount: float
    unit: AutoReduceIntervalDtoUnit
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.value

        amount = self.amount

        unit = self.unit.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mode": mode,
                "amount": amount,
                "unit": unit,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = AutoReduceIntervalDtoMode(d.pop("mode"))

        amount = d.pop("amount")

        unit = AutoReduceIntervalDtoUnit(d.pop("unit"))

        auto_reduce_interval_dto = cls(
            mode=mode,
            amount=amount,
            unit=unit,
        )

        auto_reduce_interval_dto.additional_properties = d
        return auto_reduce_interval_dto

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
