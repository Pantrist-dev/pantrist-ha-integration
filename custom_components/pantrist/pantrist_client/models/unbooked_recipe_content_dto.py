from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="UnbookedRecipeContentDto")


@_attrs_define
class UnbookedRecipeContentDto:
    """
    Attributes:
        item_id (str):
        name (str):
        content (float): Reserved content the stock could not cover, in the item's own unit.
    """

    item_id: str
    name: str
    content: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        item_id = self.item_id

        name = self.name

        content = self.content

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "itemId": item_id,
                "name": name,
                "content": content,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        item_id = d.pop("itemId")

        name = d.pop("name")

        content = d.pop("content")

        unbooked_recipe_content_dto = cls(
            item_id=item_id,
            name=name,
            content=content,
        )

        unbooked_recipe_content_dto.additional_properties = d
        return unbooked_recipe_content_dto

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
