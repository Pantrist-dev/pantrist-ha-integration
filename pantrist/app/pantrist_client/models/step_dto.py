from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.ingredient_dto import IngredientDto


T = TypeVar("T", bound="StepDto")


@_attrs_define
class StepDto:
    """
    Attributes:
        text (str): Instruction text for this step Example: Mix all dry ingredients together..
        ingredients (list[IngredientDto]): Ingredients used in this step
        partial_step_uid (str | Unset): Optional reference to a partial step
    """

    text: str
    ingredients: list[IngredientDto]
    partial_step_uid: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        ingredients = []
        for ingredients_item_data in self.ingredients:
            ingredients_item = ingredients_item_data.to_dict()
            ingredients.append(ingredients_item)

        partial_step_uid = self.partial_step_uid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
                "ingredients": ingredients,
            }
        )
        if partial_step_uid is not UNSET:
            field_dict["partialStepUid"] = partial_step_uid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.ingredient_dto import IngredientDto

        d = dict(src_dict)
        text = d.pop("text")

        ingredients = []
        _ingredients = d.pop("ingredients")
        for ingredients_item_data in _ingredients:
            ingredients_item = IngredientDto.from_dict(ingredients_item_data)

            ingredients.append(ingredients_item)

        partial_step_uid = d.pop("partialStepUid", UNSET)

        step_dto = cls(
            text=text,
            ingredients=ingredients,
            partial_step_uid=partial_step_uid,
        )

        step_dto.additional_properties = d
        return step_dto

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
