from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.weighing_unit import WeighingUnit
from ..types import UNSET, Unset

T = TypeVar("T", bound="WeighingDto")


@_attrs_define
class WeighingDto:
    """
    Attributes:
        unit (WeighingUnit): The unit the scale shows, used for `tare` and for input.
        tare (float | None | Unset): Weight of the empty container, in `unit`.
    """

    unit: WeighingUnit
    tare: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        unit = self.unit.value

        tare: float | None | Unset
        if isinstance(self.tare, Unset):
            tare = UNSET
        else:
            tare = self.tare

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "unit": unit,
            }
        )
        if tare is not UNSET:
            field_dict["tare"] = tare

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        unit = WeighingUnit(d.pop("unit"))

        def _parse_tare(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        tare = _parse_tare(d.pop("tare", UNSET))

        weighing_dto = cls(
            unit=unit,
            tare=tare,
        )

        weighing_dto.additional_properties = d
        return weighing_dto

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
