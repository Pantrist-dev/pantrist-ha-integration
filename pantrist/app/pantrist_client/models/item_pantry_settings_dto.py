from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pantry_settings_dto import PantrySettingsDto
    from ..models.saved_for_recipe_dto import SavedForRecipeDto


T = TypeVar("T", bound="ItemPantrySettingsDto")


@_attrs_define
class ItemPantrySettingsDto:
    """
    Attributes:
        article_list (list[PantrySettingsDto]):
        automatically_added_amount (float | Unset):
        old_pantry (str | Unset):
        earliest_best_before (str | Unset):
        saved_for_recipe (list[SavedForRecipeDto] | Unset):
    """

    article_list: list[PantrySettingsDto]
    automatically_added_amount: float | Unset = UNSET
    old_pantry: str | Unset = UNSET
    earliest_best_before: str | Unset = UNSET
    saved_for_recipe: list[SavedForRecipeDto] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        article_list = []
        for article_list_item_data in self.article_list:
            article_list_item = article_list_item_data.to_dict()
            article_list.append(article_list_item)

        automatically_added_amount = self.automatically_added_amount

        old_pantry = self.old_pantry

        earliest_best_before = self.earliest_best_before

        saved_for_recipe: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.saved_for_recipe, Unset):
            saved_for_recipe = []
            for saved_for_recipe_item_data in self.saved_for_recipe:
                saved_for_recipe_item = saved_for_recipe_item_data.to_dict()
                saved_for_recipe.append(saved_for_recipe_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "articleList": article_list,
            }
        )
        if automatically_added_amount is not UNSET:
            field_dict["automaticallyAddedAmount"] = automatically_added_amount
        if old_pantry is not UNSET:
            field_dict["oldPantry"] = old_pantry
        if earliest_best_before is not UNSET:
            field_dict["earliestBestBefore"] = earliest_best_before
        if saved_for_recipe is not UNSET:
            field_dict["savedForRecipe"] = saved_for_recipe

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pantry_settings_dto import PantrySettingsDto
        from ..models.saved_for_recipe_dto import SavedForRecipeDto

        d = dict(src_dict)
        article_list = []
        _article_list = d.pop("articleList")
        for article_list_item_data in _article_list:
            article_list_item = PantrySettingsDto.from_dict(article_list_item_data)

            article_list.append(article_list_item)

        automatically_added_amount = d.pop("automaticallyAddedAmount", UNSET)

        old_pantry = d.pop("oldPantry", UNSET)

        earliest_best_before = d.pop("earliestBestBefore", UNSET)

        _saved_for_recipe = d.pop("savedForRecipe", UNSET)
        saved_for_recipe: list[SavedForRecipeDto] | Unset = UNSET
        if _saved_for_recipe is not UNSET:
            saved_for_recipe = []
            for saved_for_recipe_item_data in _saved_for_recipe:
                saved_for_recipe_item = SavedForRecipeDto.from_dict(saved_for_recipe_item_data)

                saved_for_recipe.append(saved_for_recipe_item)

        item_pantry_settings_dto = cls(
            article_list=article_list,
            automatically_added_amount=automatically_added_amount,
            old_pantry=old_pantry,
            earliest_best_before=earliest_best_before,
            saved_for_recipe=saved_for_recipe,
        )

        item_pantry_settings_dto.additional_properties = d
        return item_pantry_settings_dto

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
