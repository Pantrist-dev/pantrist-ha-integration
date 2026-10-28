from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ParseNutrimentsIngredientDto")


@_attrs_define
class ParseNutrimentsIngredientDto:
    """
    Attributes:
        name (str): Ingredient name as the recipe lists it.
        content_volume (float | Unset): Amount in `volumeUnit`.
        volume_unit (str | Unset): Unit of the amount, e.g. `g`.
    """

    name: str
    content_volume: float | Unset = UNSET
    volume_unit: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        content_volume = self.content_volume

        volume_unit = self.volume_unit

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if content_volume is not UNSET:
            field_dict["contentVolume"] = content_volume
        if volume_unit is not UNSET:
            field_dict["volumeUnit"] = volume_unit

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        content_volume = d.pop("contentVolume", UNSET)

        volume_unit = d.pop("volumeUnit", UNSET)

        parse_nutriments_ingredient_dto = cls(
            name=name,
            content_volume=content_volume,
            volume_unit=volume_unit,
        )

        parse_nutriments_ingredient_dto.additional_properties = d
        return parse_nutriments_ingredient_dto

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
