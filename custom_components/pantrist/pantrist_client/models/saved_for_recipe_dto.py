from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SavedForRecipeDto")


@_attrs_define
class SavedForRecipeDto:
    """
    Attributes:
        recipe_uuid (str): Groups the reservations of one recipe. A Pantrist recipe uuid, or an id of the caller's
            choosing for a recipe that only exists outside of Pantrist.
        recipe_name (str | Unset): Display name for a recipe that only exists outside of Pantrist, where `recipeUuid`
            has no recipe to look the name up in.
        amount_saved (float | Unset):
        content_saved (float | Unset):
    """

    recipe_uuid: str
    recipe_name: str | Unset = UNSET
    amount_saved: float | Unset = UNSET
    content_saved: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_uuid = self.recipe_uuid

        recipe_name = self.recipe_name

        amount_saved = self.amount_saved

        content_saved = self.content_saved

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeUuid": recipe_uuid,
            }
        )
        if recipe_name is not UNSET:
            field_dict["recipeName"] = recipe_name
        if amount_saved is not UNSET:
            field_dict["amountSaved"] = amount_saved
        if content_saved is not UNSET:
            field_dict["contentSaved"] = content_saved

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipe_uuid = d.pop("recipeUuid")

        recipe_name = d.pop("recipeName", UNSET)

        amount_saved = d.pop("amountSaved", UNSET)

        content_saved = d.pop("contentSaved", UNSET)

        saved_for_recipe_dto = cls(
            recipe_uuid=recipe_uuid,
            recipe_name=recipe_name,
            amount_saved=amount_saved,
            content_saved=content_saved,
        )

        saved_for_recipe_dto.additional_properties = d
        return saved_for_recipe_dto

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
