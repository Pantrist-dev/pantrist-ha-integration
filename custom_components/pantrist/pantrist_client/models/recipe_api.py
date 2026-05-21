from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RecipeApi")


@_attrs_define
class RecipeApi:
    """
    Attributes:
        name (str):
        cooking_time (float):
        preparation_time (float):
        default_servings (float):
        categories (list[str]):
        ingredients (list[str]):
        steps (list[str]):
        link (str):
        image_url (str):
        description (str):
    """

    name: str
    cooking_time: float
    preparation_time: float
    default_servings: float
    categories: list[str]
    ingredients: list[str]
    steps: list[str]
    link: str
    image_url: str
    description: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        cooking_time = self.cooking_time

        preparation_time = self.preparation_time

        default_servings = self.default_servings

        categories = self.categories

        ingredients = self.ingredients

        steps = self.steps

        link = self.link

        image_url = self.image_url

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "cookingTime": cooking_time,
                "preparationTime": preparation_time,
                "defaultServings": default_servings,
                "categories": categories,
                "ingredients": ingredients,
                "steps": steps,
                "link": link,
                "imageUrl": image_url,
                "description": description,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        cooking_time = d.pop("cookingTime")

        preparation_time = d.pop("preparationTime")

        default_servings = d.pop("defaultServings")

        categories = cast(list[str], d.pop("categories"))

        ingredients = cast(list[str], d.pop("ingredients"))

        steps = cast(list[str], d.pop("steps"))

        link = d.pop("link")

        image_url = d.pop("imageUrl")

        description = d.pop("description")

        recipe_api = cls(
            name=name,
            cooking_time=cooking_time,
            preparation_time=preparation_time,
            default_servings=default_servings,
            categories=categories,
            ingredients=ingredients,
            steps=steps,
            link=link,
            image_url=image_url,
            description=description,
        )

        recipe_api.additional_properties = d
        return recipe_api

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
