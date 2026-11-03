from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.emergency_supply_group_dto_status import EmergencySupplyGroupDtoStatus
from ..models.emergency_supply_group_dto_unit import EmergencySupplyGroupDtoUnit

T = TypeVar("T", bound="EmergencySupplyGroupDto")


@_attrs_define
class EmergencySupplyGroupDto:
    """
    Attributes:
        id (str): Group of the standard, e.g. `grains` or `beverages` (BMEL) or `cereals` (WFP).
        days (float): How many days the stock of this group lasts.
        status (EmergencySupplyGroupDtoStatus): critical below 5 days, warning below 10, ok from 10 on.
        current_amount (float): Stock counted towards the group, in `unit`.
        required_amount (float): What the group needs for ten days, for everyone, in `unit`.
        unit (EmergencySupplyGroupDtoUnit):
        article_count (float): Pantry items counted in this group.
    """

    id: str
    days: float
    status: EmergencySupplyGroupDtoStatus
    current_amount: float
    required_amount: float
    unit: EmergencySupplyGroupDtoUnit
    article_count: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        days = self.days

        status = self.status.value

        current_amount = self.current_amount

        required_amount = self.required_amount

        unit = self.unit.value

        article_count = self.article_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "days": days,
                "status": status,
                "currentAmount": current_amount,
                "requiredAmount": required_amount,
                "unit": unit,
                "articleCount": article_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        days = d.pop("days")

        status = EmergencySupplyGroupDtoStatus(d.pop("status"))

        current_amount = d.pop("currentAmount")

        required_amount = d.pop("requiredAmount")

        unit = EmergencySupplyGroupDtoUnit(d.pop("unit"))

        article_count = d.pop("articleCount")

        emergency_supply_group_dto = cls(
            id=id,
            days=days,
            status=status,
            current_amount=current_amount,
            required_amount=required_amount,
            unit=unit,
            article_count=article_count,
        )

        emergency_supply_group_dto.additional_properties = d
        return emergency_supply_group_dto

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
