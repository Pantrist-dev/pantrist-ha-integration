from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CookRecipeReservationDto")


@_attrs_define
class CookRecipeReservationDto:
    """
    Attributes:
        auto_restock (bool | Unset): Add every item that drops to or below its minimum to the shopping list, as on
            `change-amount`. Default: False.
    """

    auto_restock: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        auto_restock = self.auto_restock

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auto_restock is not UNSET:
            field_dict["autoRestock"] = auto_restock

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        auto_restock = d.pop("autoRestock", UNSET)

        cook_recipe_reservation_dto = cls(
            auto_restock=auto_restock,
        )

        cook_recipe_reservation_dto.additional_properties = d
        return cook_recipe_reservation_dto

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
