from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.week_plan_receipt_dto import WeekPlanReceiptDto


T = TypeVar("T", bound="WeekPlanDayDto")


@_attrs_define
class WeekPlanDayDto:
    """
    Attributes:
        date (str): ISO date string (YYYY-MM-DD)
        list_ (list[WeekPlanReceiptDto]):
    """

    date: str
    list_: list[WeekPlanReceiptDto]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date = self.date

        list_ = []
        for list_item_data in self.list_:
            list_item = list_item_data.to_dict()
            list_.append(list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date": date,
                "list": list_,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.week_plan_receipt_dto import WeekPlanReceiptDto

        d = dict(src_dict)
        date = d.pop("date")

        list_ = []
        _list_ = d.pop("list")
        for list_item_data in _list_:
            list_item = WeekPlanReceiptDto.from_dict(list_item_data)

            list_.append(list_item)

        week_plan_day_dto = cls(
            date=date,
            list_=list_,
        )

        week_plan_day_dto.additional_properties = d
        return week_plan_day_dto

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
