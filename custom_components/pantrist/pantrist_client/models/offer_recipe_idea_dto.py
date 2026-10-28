from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offer_recipe_ingredient_dto import OfferRecipeIngredientDto
    from ..models.recipe_dto import RecipeDto


T = TypeVar("T", bound="OfferRecipeIdeaDto")


@_attrs_define
class OfferRecipeIdeaDto:
    """
    Attributes:
        recipe (RecipeDto):
        is_own (bool): True when the recipe is the caller's own. Own recipes take part like any other, private ones
            included, and rank ahead of others with the same coverage.
        ingredient_offers (list[OfferRecipeIngredientDto]): Every ingredient of the recipe, with the offer covering it
            where there is one.
        matched_ingredient_count (float): How many of the recipe's non-staple ingredients are on offer right now.
        ingredient_count (float): How many non-staple ingredients the recipe has. Salt, oil and water are excluded from
            both counts, so a recipe is not punished for needing them.
        cost_is_estimate (bool): Always true. Every price here is an estimate from the offers currently on the shelf,
            and the app must label it as one. It is computed per request, so it never goes stale, it just changes.
        store_names (list[str]): Stores the matched offers are at.
        diet_hidden_count (float | Unset): How many offers the reader's diet kept off this recipe. Present only when it
            kept some. It exists because an offer that was filtered away looks exactly like one that never existed, and the
            chain behind the filter (catalog entry, classification, matching) can be wrong in ways nobody would ever find
            out about. With a number, a page can say that something is missing and offer to show it. Example: 5.
        total_cost_cents (float | Unset): Sum of the per-ingredient shares, in cents. Only ingredients actually on offer
            contribute, so this is a floor for the shopping bill, not the bill.
        cost_per_serving_cents (float | Unset): Estimated cost per serving, in cents.
        valid_to (str | Unset): Last day all the matched offers are still valid (ISO date), i.e. the earliest end among
            them.
    """

    recipe: RecipeDto
    is_own: bool
    ingredient_offers: list[OfferRecipeIngredientDto]
    matched_ingredient_count: float
    ingredient_count: float
    cost_is_estimate: bool
    store_names: list[str]
    diet_hidden_count: float | Unset = UNSET
    total_cost_cents: float | Unset = UNSET
    cost_per_serving_cents: float | Unset = UNSET
    valid_to: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe = self.recipe.to_dict()

        is_own = self.is_own

        ingredient_offers = []
        for ingredient_offers_item_data in self.ingredient_offers:
            ingredient_offers_item = ingredient_offers_item_data.to_dict()
            ingredient_offers.append(ingredient_offers_item)

        matched_ingredient_count = self.matched_ingredient_count

        ingredient_count = self.ingredient_count

        cost_is_estimate = self.cost_is_estimate

        store_names = self.store_names

        diet_hidden_count = self.diet_hidden_count

        total_cost_cents = self.total_cost_cents

        cost_per_serving_cents = self.cost_per_serving_cents

        valid_to = self.valid_to

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipe": recipe,
                "isOwn": is_own,
                "ingredientOffers": ingredient_offers,
                "matchedIngredientCount": matched_ingredient_count,
                "ingredientCount": ingredient_count,
                "costIsEstimate": cost_is_estimate,
                "storeNames": store_names,
            }
        )
        if diet_hidden_count is not UNSET:
            field_dict["dietHiddenCount"] = diet_hidden_count
        if total_cost_cents is not UNSET:
            field_dict["totalCostCents"] = total_cost_cents
        if cost_per_serving_cents is not UNSET:
            field_dict["costPerServingCents"] = cost_per_serving_cents
        if valid_to is not UNSET:
            field_dict["validTo"] = valid_to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offer_recipe_ingredient_dto import OfferRecipeIngredientDto  # noqa: PLC0415
        from ..models.recipe_dto import RecipeDto  # noqa: PLC0415

        d = dict(src_dict)
        recipe = RecipeDto.from_dict(d.pop("recipe"))

        is_own = d.pop("isOwn")

        ingredient_offers = []
        _ingredient_offers = d.pop("ingredientOffers")
        for ingredient_offers_item_data in _ingredient_offers:
            ingredient_offers_item = OfferRecipeIngredientDto.from_dict(ingredient_offers_item_data)

            ingredient_offers.append(ingredient_offers_item)

        matched_ingredient_count = d.pop("matchedIngredientCount")

        ingredient_count = d.pop("ingredientCount")

        cost_is_estimate = d.pop("costIsEstimate")

        store_names = cast(list[str], d.pop("storeNames"))

        diet_hidden_count = d.pop("dietHiddenCount", UNSET)

        total_cost_cents = d.pop("totalCostCents", UNSET)

        cost_per_serving_cents = d.pop("costPerServingCents", UNSET)

        valid_to = d.pop("validTo", UNSET)

        offer_recipe_idea_dto = cls(
            recipe=recipe,
            is_own=is_own,
            ingredient_offers=ingredient_offers,
            matched_ingredient_count=matched_ingredient_count,
            ingredient_count=ingredient_count,
            cost_is_estimate=cost_is_estimate,
            store_names=store_names,
            diet_hidden_count=diet_hidden_count,
            total_cost_cents=total_cost_cents,
            cost_per_serving_cents=cost_per_serving_cents,
            valid_to=valid_to,
        )

        offer_recipe_idea_dto.additional_properties = d
        return offer_recipe_idea_dto

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
