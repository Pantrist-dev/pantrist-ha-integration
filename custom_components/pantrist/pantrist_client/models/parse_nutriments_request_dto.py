from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parse_nutriments_ingredient_dto import ParseNutrimentsIngredientDto


T = TypeVar("T", bound="ParseNutrimentsRequestDto")


@_attrs_define
class ParseNutrimentsRequestDto:
    """
    Attributes:
        ingredients (list[ParseNutrimentsIngredientDto]):
        default_servings (float | Unset): Servings the amounts above are for. Defaults to 1. Example: 4.
        servings_unit (str | Unset): Serving unit, e.g. `Portion`. Example: Portion.
        target_language (str | Unset): Translate nothing but keep the analysis consistent with this language. BCP 47
            tag. Example: de.
    """

    ingredients: list[ParseNutrimentsIngredientDto]
    default_servings: float | Unset = UNSET
    servings_unit: str | Unset = UNSET
    target_language: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ingredients = []
        for ingredients_item_data in self.ingredients:
            ingredients_item = ingredients_item_data.to_dict()
            ingredients.append(ingredients_item)

        default_servings = self.default_servings

        servings_unit = self.servings_unit

        target_language = self.target_language

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ingredients": ingredients,
            }
        )
        if default_servings is not UNSET:
            field_dict["defaultServings"] = default_servings
        if servings_unit is not UNSET:
            field_dict["servingsUnit"] = servings_unit
        if target_language is not UNSET:
            field_dict["targetLanguage"] = target_language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.parse_nutriments_ingredient_dto import ParseNutrimentsIngredientDto  # noqa: PLC0415

        d = dict(src_dict)
        ingredients = []
        _ingredients = d.pop("ingredients")
        for ingredients_item_data in _ingredients:
            ingredients_item = ParseNutrimentsIngredientDto.from_dict(ingredients_item_data)

            ingredients.append(ingredients_item)

        default_servings = d.pop("defaultServings", UNSET)

        servings_unit = d.pop("servingsUnit", UNSET)

        target_language = d.pop("targetLanguage", UNSET)

        parse_nutriments_request_dto = cls(
            ingredients=ingredients,
            default_servings=default_servings,
            servings_unit=servings_unit,
            target_language=target_language,
        )

        parse_nutriments_request_dto.additional_properties = d
        return parse_nutriments_request_dto

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
