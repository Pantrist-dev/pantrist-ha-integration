from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RecipeMatchedIngredientDto")


@_attrs_define
class RecipeMatchedIngredientDto:
    """
    Attributes:
        recipe_ingredient_name (str): Recipe ingredient display name (from the recipe).
        pantry_item_id (str): UUID of the pantry list item that satisfied the ingredient.
        pantry_item_name (str): Name of the pantry list item.
        list_id (str): List the pantry item belongs to. Useful for deep-link routing when the app shows multiple
            households and needs to know which list to open.
    """

    recipe_ingredient_name: str
    pantry_item_id: str
    pantry_item_name: str
    list_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_ingredient_name = self.recipe_ingredient_name

        pantry_item_id = self.pantry_item_id

        pantry_item_name = self.pantry_item_name

        list_id = self.list_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeIngredientName": recipe_ingredient_name,
                "pantryItemId": pantry_item_id,
                "pantryItemName": pantry_item_name,
                "listId": list_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipe_ingredient_name = d.pop("recipeIngredientName")

        pantry_item_id = d.pop("pantryItemId")

        pantry_item_name = d.pop("pantryItemName")

        list_id = d.pop("listId")

        recipe_matched_ingredient_dto = cls(
            recipe_ingredient_name=recipe_ingredient_name,
            pantry_item_id=pantry_item_id,
            pantry_item_name=pantry_item_name,
            list_id=list_id,
        )

        recipe_matched_ingredient_dto.additional_properties = d
        return recipe_matched_ingredient_dto

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
