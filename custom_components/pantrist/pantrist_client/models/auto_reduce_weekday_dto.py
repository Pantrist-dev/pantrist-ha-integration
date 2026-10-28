from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auto_reduce_weekday_dto_mode import AutoReduceWeekdayDtoMode

T = TypeVar("T", bound="AutoReduceWeekdayDto")


@_attrs_define
class AutoReduceWeekdayDto:
    """
    Attributes:
        mode (AutoReduceWeekdayDtoMode):
        amounts (list[float]): Per-weekday amounts, ordered Monday through Sunday
    """

    mode: AutoReduceWeekdayDtoMode
    amounts: list[float]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        mode = self.mode.value

        amounts = self.amounts

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "mode": mode,
                "amounts": amounts,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        mode = AutoReduceWeekdayDtoMode(d.pop("mode"))

        amounts = cast(list[float], d.pop("amounts"))

        auto_reduce_weekday_dto = cls(
            mode=mode,
            amounts=amounts,
        )

        auto_reduce_weekday_dto.additional_properties = d
        return auto_reduce_weekday_dto

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
