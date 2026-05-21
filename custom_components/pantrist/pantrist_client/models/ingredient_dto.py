from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ingredient_dto_volume_unit import IngredientDtoVolumeUnit
from ..types import UNSET, Unset

T = TypeVar("T", bound="IngredientDto")


@_attrs_define
class IngredientDto:
    """
    Attributes:
        name (str): Ingredient name Example: Flour.
        content_volume (float): Amount of the ingredient Example: 200.
        volume_unit (IngredientDtoVolumeUnit): Unit of measurement (Pinch or volume unit) Example: g.
        notes (str | Unset): Optional notes about the ingredient
        partial_step_uid (str | Unset): Reference to a partial step UUID
    """

    name: str
    content_volume: float
    volume_unit: IngredientDtoVolumeUnit
    notes: str | Unset = UNSET
    partial_step_uid: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        content_volume = self.content_volume

        volume_unit = self.volume_unit.value

        notes = self.notes

        partial_step_uid = self.partial_step_uid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "contentVolume": content_volume,
                "volumeUnit": volume_unit,
            }
        )
        if notes is not UNSET:
            field_dict["notes"] = notes
        if partial_step_uid is not UNSET:
            field_dict["partialStepUid"] = partial_step_uid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        content_volume = d.pop("contentVolume")

        volume_unit = IngredientDtoVolumeUnit(d.pop("volumeUnit"))

        notes = d.pop("notes", UNSET)

        partial_step_uid = d.pop("partialStepUid", UNSET)

        ingredient_dto = cls(
            name=name,
            content_volume=content_volume,
            volume_unit=volume_unit,
            notes=notes,
            partial_step_uid=partial_step_uid,
        )

        ingredient_dto.additional_properties = d
        return ingredient_dto

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
