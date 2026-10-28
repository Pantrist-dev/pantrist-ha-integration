from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ingredient_dto_volume_unit import IngredientDtoVolumeUnit
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.metric_equivalent_dto import MetricEquivalentDto


T = TypeVar("T", bound="IngredientDto")


@_attrs_define
class IngredientDto:
    """
    Attributes:
        name (str): Ingredient name Example: Flour.
        content_volume (float): Amount of the ingredient Example: 200.
        volume_unit (IngredientDtoVolumeUnit): Unit of measurement (Pinch or volume unit) Example: g.
        metric_equivalent (MetricEquivalentDto | Unset):
        notes (str | Unset): Optional notes about the ingredient
        normalized_name (str | Unset): Server-derived, normalised core noun of the ingredient (language-aware:
            quantities, units and descriptors stripped, singularised). Used for stable pantry↔recipe matching and de-
            duplication; clients should treat it as read-only.
        ingredient_id (str | Unset): Server-derived canonical ingredient id: the resolved entry of the shared ingredient
            catalog. Used for stable, language-independent pantry↔recipe matching. Null when the ingredient could not be
            resolved (then matching falls back to normalizedName). Read-only for clients.
        partial_step_uid (str | Unset): Reference to a partial step UUID
    """

    name: str
    content_volume: float
    volume_unit: IngredientDtoVolumeUnit
    metric_equivalent: MetricEquivalentDto | Unset = UNSET
    notes: str | Unset = UNSET
    normalized_name: str | Unset = UNSET
    ingredient_id: str | Unset = UNSET
    partial_step_uid: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        content_volume = self.content_volume

        volume_unit = self.volume_unit.value

        metric_equivalent: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metric_equivalent, Unset):
            metric_equivalent = self.metric_equivalent.to_dict()

        notes = self.notes

        normalized_name = self.normalized_name

        ingredient_id = self.ingredient_id

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
        if metric_equivalent is not UNSET:
            field_dict["metricEquivalent"] = metric_equivalent
        if notes is not UNSET:
            field_dict["notes"] = notes
        if normalized_name is not UNSET:
            field_dict["normalizedName"] = normalized_name
        if ingredient_id is not UNSET:
            field_dict["ingredientId"] = ingredient_id
        if partial_step_uid is not UNSET:
            field_dict["partialStepUid"] = partial_step_uid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.metric_equivalent_dto import MetricEquivalentDto  # noqa: PLC0415

        d = dict(src_dict)
        name = d.pop("name")

        content_volume = d.pop("contentVolume")

        volume_unit = IngredientDtoVolumeUnit(d.pop("volumeUnit"))

        _metric_equivalent = d.pop("metricEquivalent", UNSET)
        metric_equivalent: MetricEquivalentDto | Unset
        if isinstance(_metric_equivalent, Unset) or _metric_equivalent is None:
            metric_equivalent = UNSET
        else:
            metric_equivalent = MetricEquivalentDto.from_dict(_metric_equivalent)

        notes = d.pop("notes", UNSET)

        normalized_name = d.pop("normalizedName", UNSET)

        ingredient_id = d.pop("ingredientId", UNSET)

        partial_step_uid = d.pop("partialStepUid", UNSET)

        ingredient_dto = cls(
            name=name,
            content_volume=content_volume,
            volume_unit=volume_unit,
            metric_equivalent=metric_equivalent,
            notes=notes,
            normalized_name=normalized_name,
            ingredient_id=ingredient_id,
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
