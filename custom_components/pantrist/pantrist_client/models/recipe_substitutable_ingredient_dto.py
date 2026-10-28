from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.recipe_substitutable_ingredient_dto_confidence import RecipeSubstitutableIngredientDtoConfidence
from ..models.recipe_substitutable_ingredient_dto_kind import RecipeSubstitutableIngredientDtoKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="RecipeSubstitutableIngredientDto")


@_attrs_define
class RecipeSubstitutableIngredientDto:
    """
    Attributes:
        recipe_ingredient_name (str): Recipe ingredient display name (from the recipe).
        pantry_item_id (str): UUID of the pantry list item the user can substitute with.
        pantry_item_name (str): Name of the pantry list item (e.g. "Margarine").
        list_id (str): List the substitute pantry item belongs to (deep-link routing).
        confidence (RecipeSubstitutableIngredientDtoConfidence): How well the substitute covers the target: `perfect`
            (1:1, indistinguishable), `good` (clear shift but same role), `emergency` (last-resort).
        note (str | Unset): Optional localised hint resolved to the caller language with en-US fallback ("1:1 swap",
            "Vegane Variante, 1:1 ersetzbar"). Missing when the curated row had no note for any locale.
        kind (RecipeSubstitutableIngredientDtoKind | Unset): Why the pantry item can stand in: `variant` — the pantry
            holds a more generic kind of the requested ingredient (Tomaten for Kirschtomaten); `substitute` — a curated
            substitution edge. Older API builds omit it (treat as `substitute`).
    """

    recipe_ingredient_name: str
    pantry_item_id: str
    pantry_item_name: str
    list_id: str
    confidence: RecipeSubstitutableIngredientDtoConfidence
    note: str | Unset = UNSET
    kind: RecipeSubstitutableIngredientDtoKind | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_ingredient_name = self.recipe_ingredient_name

        pantry_item_id = self.pantry_item_id

        pantry_item_name = self.pantry_item_name

        list_id = self.list_id

        confidence = self.confidence.value

        note = self.note

        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeIngredientName": recipe_ingredient_name,
                "pantryItemId": pantry_item_id,
                "pantryItemName": pantry_item_name,
                "listId": list_id,
                "confidence": confidence,
            }
        )
        if note is not UNSET:
            field_dict["note"] = note
        if kind is not UNSET:
            field_dict["kind"] = kind

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipe_ingredient_name = d.pop("recipeIngredientName")

        pantry_item_id = d.pop("pantryItemId")

        pantry_item_name = d.pop("pantryItemName")

        list_id = d.pop("listId")

        confidence = RecipeSubstitutableIngredientDtoConfidence(d.pop("confidence"))

        note = d.pop("note", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: RecipeSubstitutableIngredientDtoKind | Unset
        if isinstance(_kind, Unset) or _kind is None or _kind == "":
            kind = UNSET
        else:
            kind = RecipeSubstitutableIngredientDtoKind(_kind)

        recipe_substitutable_ingredient_dto = cls(
            recipe_ingredient_name=recipe_ingredient_name,
            pantry_item_id=pantry_item_id,
            pantry_item_name=pantry_item_name,
            list_id=list_id,
            confidence=confidence,
            note=note,
            kind=kind,
        )

        recipe_substitutable_ingredient_dto.additional_properties = d
        return recipe_substitutable_ingredient_dto

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
