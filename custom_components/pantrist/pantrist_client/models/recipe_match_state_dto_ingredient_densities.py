from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RecipeMatchStateDtoIngredientDensities")


@_attrs_define
class RecipeMatchStateDtoIngredientDensities:
    """Grams per millilitre for the recipe ingredients whose catalog entry has been measured, keyed by display name. Lets
    the app weigh a recipe's spoon against a pantry item kept by the gram: one tablespoon is 15 ml, so 15 ml of paprika
    powder at 0.45 is about 7 g. Only the ingredients with a known density appear; for the rest the app keeps its old
    behaviour and treats a stocked pantry item as covering the ingredient without deducting from it.

        Example:
            {'Paprikapulver': 0.45, 'Olivenöl': 0.91}

    """

    additional_properties: dict[str, float] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipe_match_state_dto_ingredient_densities = cls()

        recipe_match_state_dto_ingredient_densities.additional_properties = d
        return recipe_match_state_dto_ingredient_densities

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> float:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: float) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
