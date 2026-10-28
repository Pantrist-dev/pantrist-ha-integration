from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.offer_ingredient_match_dto_allergens_item import OfferIngredientMatchDtoAllergensItem
from ..models.offer_ingredient_match_dto_diet import OfferIngredientMatchDtoDiet
from ..models.offer_ingredient_match_dto_match_method import OfferIngredientMatchDtoMatchMethod
from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferIngredientMatchDto")


@_attrs_define
class OfferIngredientMatchDto:
    """
    Attributes:
        ingredient_id (str): Ingredient id in the Pantrist catalog.
        name (str): Localised catalog name in the requested language.
        confidence (float): 0..1. Below 0.6 the app must hedge the wording.
        match_method (OfferIngredientMatchDtoMatchMethod):
        diet (OfferIngredientMatchDtoDiet | Unset): What the catalog says this ingredient contains: vegan, vegetarian
            (animal produce but no flesh), fish or meat. Absent while nobody has classified the entry.

            Sent rather than applied, because this endpoint is anonymous and publicly cached: one filtered answer must never
            be served to the next reader. A client that knows what its user eats can filter on it, and the answer stays the
            same for everybody.
        allergens (list[OfferIngredientMatchDtoAllergensItem] | Unset): Declarable allergens the catalog names for this
            ingredient. An empty list means none were named, which is not a statement that the product is safe, and no
            client may present it as one.
    """

    ingredient_id: str
    name: str
    confidence: float
    match_method: OfferIngredientMatchDtoMatchMethod
    diet: OfferIngredientMatchDtoDiet | Unset = UNSET
    allergens: list[OfferIngredientMatchDtoAllergensItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ingredient_id = self.ingredient_id

        name = self.name

        confidence = self.confidence

        match_method = self.match_method.value

        diet: str | Unset = UNSET
        if not isinstance(self.diet, Unset):
            diet = self.diet.value

        allergens: list[str] | Unset = UNSET
        if not isinstance(self.allergens, Unset):
            allergens = []
            for allergens_item_data in self.allergens:
                allergens_item = allergens_item_data.value
                allergens.append(allergens_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ingredientId": ingredient_id,
                "name": name,
                "confidence": confidence,
                "matchMethod": match_method,
            }
        )
        if diet is not UNSET:
            field_dict["diet"] = diet
        if allergens is not UNSET:
            field_dict["allergens"] = allergens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ingredient_id = d.pop("ingredientId")

        name = d.pop("name")

        confidence = d.pop("confidence")

        match_method = OfferIngredientMatchDtoMatchMethod(d.pop("matchMethod"))

        _diet = d.pop("diet", UNSET)
        diet: OfferIngredientMatchDtoDiet | Unset
        if isinstance(_diet, Unset) or _diet is None or _diet == "":
            diet = UNSET
        else:
            diet = OfferIngredientMatchDtoDiet(_diet)

        _allergens = d.pop("allergens", UNSET)
        allergens: list[OfferIngredientMatchDtoAllergensItem] | Unset = UNSET
        if _allergens is not UNSET:
            allergens = []
            for allergens_item_data in _allergens:
                allergens_item = OfferIngredientMatchDtoAllergensItem(allergens_item_data)

                allergens.append(allergens_item)

        offer_ingredient_match_dto = cls(
            ingredient_id=ingredient_id,
            name=name,
            confidence=confidence,
            match_method=match_method,
            diet=diet,
            allergens=allergens,
        )

        offer_ingredient_match_dto.additional_properties = d
        return offer_ingredient_match_dto

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
