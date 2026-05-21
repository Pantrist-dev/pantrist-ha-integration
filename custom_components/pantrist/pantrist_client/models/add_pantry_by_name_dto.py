from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddPantryByNameDto")


@_attrs_define
class AddPantryByNameDto:
    """
    Attributes:
        name (str):
        amount (float | Unset):  Default: 1.0.
        unit_id (str | Unset):  Default: 'pieces'.
    """

    name: str
    amount: float | Unset = 1.0
    unit_id: str | Unset = "pieces"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        amount = self.amount

        unit_id = self.unit_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if amount is not UNSET:
            field_dict["amount"] = amount
        if unit_id is not UNSET:
            field_dict["unitId"] = unit_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        amount = d.pop("amount", UNSET)

        unit_id = d.pop("unitId", UNSET)

        add_pantry_by_name_dto = cls(
            name=name,
            amount=amount,
            unit_id=unit_id,
        )

        add_pantry_by_name_dto.additional_properties = d
        return add_pantry_by_name_dto

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
