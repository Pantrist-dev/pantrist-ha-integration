from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.recipe_parsing_result_dto import RecipeParsingResultDto


T = TypeVar("T", bound="RecipeParsingCollectionResultDto")


@_attrs_define
class RecipeParsingCollectionResultDto:
    """
    Attributes:
        recipes (list[RecipeParsingResultDto]): Every recipe found, in source order. Empty when the input held no
            recipe.
        source_count (float): How many recipe candidates the source contained before the per-import cap: image groups
            for photos and carousels, entries for an export file.
        skipped_count (float): Candidates beyond the per-import cap that were not parsed. The client can tell the user
            to import the rest separately.
        skipped_page_count (float | Unset): PDF pages beyond the per-import page cap that were not read. Absent or 0
            when every page was read.
    """

    recipes: list[RecipeParsingResultDto]
    source_count: float
    skipped_count: float
    skipped_page_count: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipes = []
        for recipes_item_data in self.recipes:
            recipes_item = recipes_item_data.to_dict()
            recipes.append(recipes_item)

        source_count = self.source_count

        skipped_count = self.skipped_count

        skipped_page_count = self.skipped_page_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipes": recipes,
                "sourceCount": source_count,
                "skippedCount": skipped_count,
            }
        )
        if skipped_page_count is not UNSET:
            field_dict["skippedPageCount"] = skipped_page_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.recipe_parsing_result_dto import RecipeParsingResultDto  # noqa: PLC0415

        d = dict(src_dict)
        recipes = []
        _recipes = d.pop("recipes")
        for recipes_item_data in _recipes:
            recipes_item = RecipeParsingResultDto.from_dict(recipes_item_data)

            recipes.append(recipes_item)

        source_count = d.pop("sourceCount")

        skipped_count = d.pop("skippedCount")

        skipped_page_count = d.pop("skippedPageCount", UNSET)

        recipe_parsing_collection_result_dto = cls(
            recipes=recipes,
            source_count=source_count,
            skipped_count=skipped_count,
            skipped_page_count=skipped_page_count,
        )

        recipe_parsing_collection_result_dto.additional_properties = d
        return recipe_parsing_collection_result_dto

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
