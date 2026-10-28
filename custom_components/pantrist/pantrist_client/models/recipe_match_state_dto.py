from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.recipe_match_state_dto_ingredient_densities import RecipeMatchStateDtoIngredientDensities
    from ..models.recipe_matched_ingredient_dto import RecipeMatchedIngredientDto
    from ..models.recipe_substitutable_ingredient_dto import RecipeSubstitutableIngredientDto


T = TypeVar("T", bound="RecipeMatchStateDto")


@_attrs_define
class RecipeMatchStateDto:
    """
    Attributes:
        uuid (str): Recipe UUID
        matching_count (float): Count of ingredients that are either in the pantry or count as staples (always-
            available) for the recipe language.
        ingredient_count (float): Total ingredient count of the recipe
        missing_ingredients (list[str] | Unset): Names of ingredients not covered by the pantry (excl. staples)
        matched_ingredients (list[RecipeMatchedIngredientDto] | Unset): Per-ingredient pantry-side detail for the
            ingredients the recipe matched. Lets the app render "Butter — durch deine Margarine ersetzt" with a deep link to
            the pantry item instead of inferring the mapping by name client-side. Staples are not included (they always
            count as available but aren't tied to a specific pantry item).
        staple_ingredients (list[str] | Unset): Display names of recipe ingredients flagged as staples for the recipe
            language (salt, water, oil, …). Staples count toward `matchingCount` because they're assumed always-available,
            but they don't link to a specific pantry item. The app uses this list to render "Du hast das wahrscheinlich
            zuhause" instead of the regular "Du hast X im Vorrat" line.
        substitutable_ingredients (list[RecipeSubstitutableIngredientDto] | Unset): Recipe ingredients the user can
            cover via a curated substitution (Stufe 2c) — Margarine for Butter, Honey for Maple syrup, etc. Entries move out
            of `missingIngredients` so the app can render them in a distinct "can substitute" bucket (yellow) rather than as
            plain misses (red). `matchingCount` stays honest: substitutables do NOT count as direct matches — they're a
            weaker signal.
        ingredient_densities (RecipeMatchStateDtoIngredientDensities | Unset): Grams per millilitre for the recipe
            ingredients whose catalog entry has been measured, keyed by display name. Lets the app weigh a recipe's spoon
            against a pantry item kept by the gram: one tablespoon is 15 ml, so 15 ml of paprika powder at 0.45 is about 7
            g. Only the ingredients with a known density appear; for the rest the app keeps its old behaviour and treats a
            stocked pantry item as covering the ingredient without deducting from it. Example: {'Paprikapulver': 0.45,
            'Olivenöl': 0.91}.
    """

    uuid: str
    matching_count: float
    ingredient_count: float
    missing_ingredients: list[str] | Unset = UNSET
    matched_ingredients: list[RecipeMatchedIngredientDto] | Unset = UNSET
    staple_ingredients: list[str] | Unset = UNSET
    substitutable_ingredients: list[RecipeSubstitutableIngredientDto] | Unset = UNSET
    ingredient_densities: RecipeMatchStateDtoIngredientDensities | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        matching_count = self.matching_count

        ingredient_count = self.ingredient_count

        missing_ingredients: list[str] | Unset = UNSET
        if not isinstance(self.missing_ingredients, Unset):
            missing_ingredients = self.missing_ingredients

        matched_ingredients: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.matched_ingredients, Unset):
            matched_ingredients = []
            for matched_ingredients_item_data in self.matched_ingredients:
                matched_ingredients_item = matched_ingredients_item_data.to_dict()
                matched_ingredients.append(matched_ingredients_item)

        staple_ingredients: list[str] | Unset = UNSET
        if not isinstance(self.staple_ingredients, Unset):
            staple_ingredients = self.staple_ingredients

        substitutable_ingredients: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.substitutable_ingredients, Unset):
            substitutable_ingredients = []
            for substitutable_ingredients_item_data in self.substitutable_ingredients:
                substitutable_ingredients_item = substitutable_ingredients_item_data.to_dict()
                substitutable_ingredients.append(substitutable_ingredients_item)

        ingredient_densities: dict[str, Any] | Unset = UNSET
        if not isinstance(self.ingredient_densities, Unset):
            ingredient_densities = self.ingredient_densities.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "matchingCount": matching_count,
                "ingredientCount": ingredient_count,
            }
        )
        if missing_ingredients is not UNSET:
            field_dict["missingIngredients"] = missing_ingredients
        if matched_ingredients is not UNSET:
            field_dict["matchedIngredients"] = matched_ingredients
        if staple_ingredients is not UNSET:
            field_dict["stapleIngredients"] = staple_ingredients
        if substitutable_ingredients is not UNSET:
            field_dict["substitutableIngredients"] = substitutable_ingredients
        if ingredient_densities is not UNSET:
            field_dict["ingredientDensities"] = ingredient_densities

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_match_state_dto_ingredient_densities import RecipeMatchStateDtoIngredientDensities  # noqa: PLC0415
        from ..models.recipe_matched_ingredient_dto import RecipeMatchedIngredientDto  # noqa: PLC0415
        from ..models.recipe_substitutable_ingredient_dto import RecipeSubstitutableIngredientDto  # noqa: PLC0415

        d = dict(src_dict)
        uuid = d.pop("uuid")

        matching_count = d.pop("matchingCount")

        ingredient_count = d.pop("ingredientCount")

        missing_ingredients = cast(list[str], d.pop("missingIngredients", UNSET))

        _matched_ingredients = d.pop("matchedIngredients", UNSET)
        matched_ingredients: list[RecipeMatchedIngredientDto] | Unset = UNSET
        if _matched_ingredients is not UNSET:
            matched_ingredients = []
            for matched_ingredients_item_data in _matched_ingredients:
                matched_ingredients_item = RecipeMatchedIngredientDto.from_dict(matched_ingredients_item_data)

                matched_ingredients.append(matched_ingredients_item)

        staple_ingredients = cast(list[str], d.pop("stapleIngredients", UNSET))

        _substitutable_ingredients = d.pop("substitutableIngredients", UNSET)
        substitutable_ingredients: list[RecipeSubstitutableIngredientDto] | Unset = UNSET
        if _substitutable_ingredients is not UNSET:
            substitutable_ingredients = []
            for substitutable_ingredients_item_data in _substitutable_ingredients:
                substitutable_ingredients_item = RecipeSubstitutableIngredientDto.from_dict(
                    substitutable_ingredients_item_data
                )

                substitutable_ingredients.append(substitutable_ingredients_item)

        _ingredient_densities = d.pop("ingredientDensities", UNSET)
        ingredient_densities: RecipeMatchStateDtoIngredientDensities | Unset
        if isinstance(_ingredient_densities, Unset) or _ingredient_densities is None:
            ingredient_densities = UNSET
        else:
            ingredient_densities = RecipeMatchStateDtoIngredientDensities.from_dict(_ingredient_densities)

        recipe_match_state_dto = cls(
            uuid=uuid,
            matching_count=matching_count,
            ingredient_count=ingredient_count,
            missing_ingredients=missing_ingredients,
            matched_ingredients=matched_ingredients,
            staple_ingredients=staple_ingredients,
            substitutable_ingredients=substitutable_ingredients,
            ingredient_densities=ingredient_densities,
        )

        recipe_match_state_dto.additional_properties = d
        return recipe_match_state_dto

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
