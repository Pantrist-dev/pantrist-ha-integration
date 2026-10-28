from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.dietary_preferences_dto_allergens_item import DietaryPreferencesDtoAllergensItem
from ..models.dietary_preferences_dto_dietary_styles_item import DietaryPreferencesDtoDietaryStylesItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="DietaryPreferencesDto")


@_attrs_define
class DietaryPreferencesDto:
    """
    Attributes:
        dietary_styles (list[DietaryPreferencesDtoDietaryStylesItem] | Unset): Preferred dietary styles for this
            household (subset of recipe categories, e.g. Vegan, Vegetarian, Keto). Used as default OR filter.
        allergens (list[DietaryPreferencesDtoAllergensItem] | Unset): Allergens this household wants to avoid. Used to
            warn on items and to exclude recipes containing these allergens.
    """

    dietary_styles: list[DietaryPreferencesDtoDietaryStylesItem] | Unset = UNSET
    allergens: list[DietaryPreferencesDtoAllergensItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        dietary_styles: list[str] | Unset = UNSET
        if not isinstance(self.dietary_styles, Unset):
            dietary_styles = []
            for dietary_styles_item_data in self.dietary_styles:
                dietary_styles_item = dietary_styles_item_data.value
                dietary_styles.append(dietary_styles_item)

        allergens: list[str] | Unset = UNSET
        if not isinstance(self.allergens, Unset):
            allergens = []
            for allergens_item_data in self.allergens:
                allergens_item = allergens_item_data.value
                allergens.append(allergens_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if dietary_styles is not UNSET:
            field_dict["dietaryStyles"] = dietary_styles
        if allergens is not UNSET:
            field_dict["allergens"] = allergens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _dietary_styles = d.pop("dietaryStyles", UNSET)
        dietary_styles: list[DietaryPreferencesDtoDietaryStylesItem] | Unset = UNSET
        if _dietary_styles is not UNSET:
            dietary_styles = []
            for dietary_styles_item_data in _dietary_styles:
                dietary_styles_item = DietaryPreferencesDtoDietaryStylesItem(dietary_styles_item_data)

                dietary_styles.append(dietary_styles_item)

        _allergens = d.pop("allergens", UNSET)
        allergens: list[DietaryPreferencesDtoAllergensItem] | Unset = UNSET
        if _allergens is not UNSET:
            allergens = []
            for allergens_item_data in _allergens:
                allergens_item = DietaryPreferencesDtoAllergensItem(allergens_item_data)

                allergens.append(allergens_item)

        dietary_preferences_dto = cls(
            dietary_styles=dietary_styles,
            allergens=allergens,
        )

        dietary_preferences_dto.additional_properties = d
        return dietary_preferences_dto

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
