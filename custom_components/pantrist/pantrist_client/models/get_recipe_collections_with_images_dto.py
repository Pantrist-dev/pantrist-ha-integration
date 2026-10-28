from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetRecipeCollectionsWithImagesDto")


@_attrs_define
class GetRecipeCollectionsWithImagesDto:
    """
    Attributes:
        uuid (str):
        name (str):
        share_in_list (bool):
        connected_recipe_images (list[str]):
        recipe_count (float): Total number of recipes in the collection. May be larger than connectedRecipeImages.length
            because recipes without an image are still counted.
    """

    uuid: str
    name: str
    share_in_list: bool
    connected_recipe_images: list[str]
    recipe_count: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        name = self.name

        share_in_list = self.share_in_list

        connected_recipe_images = self.connected_recipe_images

        recipe_count = self.recipe_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "shareInList": share_in_list,
                "connectedRecipeImages": connected_recipe_images,
                "recipeCount": recipe_count,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        name = d.pop("name")

        share_in_list = d.pop("shareInList")

        connected_recipe_images = cast(list[str], d.pop("connectedRecipeImages"))

        recipe_count = d.pop("recipeCount")

        get_recipe_collections_with_images_dto = cls(
            uuid=uuid,
            name=name,
            share_in_list=share_in_list,
            connected_recipe_images=connected_recipe_images,
            recipe_count=recipe_count,
        )

        get_recipe_collections_with_images_dto.additional_properties = d
        return get_recipe_collections_with_images_dto

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
