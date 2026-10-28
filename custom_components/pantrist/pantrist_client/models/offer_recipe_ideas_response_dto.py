from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offer_recipe_idea_dto import OfferRecipeIdeaDto


T = TypeVar("T", bound="OfferRecipeIdeasResponseDto")


@_attrs_define
class OfferRecipeIdeasResponseDto:
    """
    Attributes:
        ideas (list[OfferRecipeIdeaDto]):
        offered_ingredient_count (float): How many catalog ingredients are on offer at the given stores. Zero means the
            empty state, not an error.
        generated_for_you (bool): True when this request triggered a generation for the caller's region and preferences
            because the pool had too little to offer. The ideas above already include what it produced.
    """

    ideas: list[OfferRecipeIdeaDto]
    offered_ingredient_count: float
    generated_for_you: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ideas = []
        for ideas_item_data in self.ideas:
            ideas_item = ideas_item_data.to_dict()
            ideas.append(ideas_item)

        offered_ingredient_count = self.offered_ingredient_count

        generated_for_you = self.generated_for_you

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ideas": ideas,
                "offeredIngredientCount": offered_ingredient_count,
                "generatedForYou": generated_for_you,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offer_recipe_idea_dto import OfferRecipeIdeaDto  # noqa: PLC0415

        d = dict(src_dict)
        ideas = []
        _ideas = d.pop("ideas")
        for ideas_item_data in _ideas:
            ideas_item = OfferRecipeIdeaDto.from_dict(ideas_item_data)

            ideas.append(ideas_item)

        offered_ingredient_count = d.pop("offeredIngredientCount")

        generated_for_you = d.pop("generatedForYou")

        offer_recipe_ideas_response_dto = cls(
            ideas=ideas,
            offered_ingredient_count=offered_ingredient_count,
            generated_for_you=generated_for_you,
        )

        offer_recipe_ideas_response_dto.additional_properties = d
        return offer_recipe_ideas_response_dto

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
