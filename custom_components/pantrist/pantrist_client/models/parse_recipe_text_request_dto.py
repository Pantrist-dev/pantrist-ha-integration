from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ParseRecipeTextRequestDto")


@_attrs_define
class ParseRecipeTextRequestDto:
    """
    Attributes:
        text (str): The raw text of the recipe to parse Example: Banana Pancakes

            Ingredients:
            - 2 bananas
            - 2 eggs

            Directions:
            1. Mash bananas....
        target_language (str | Unset): Translate the parsed recipe into this language instead of preserving the source
            language. Accepts a BCP 47 tag (e.g. `de`, `en-US`, `pt-BR`). Only the human-readable fields are translated;
            unit codes, categories and allergens stay as their canonical identifiers. Omit to keep the source language
            (default). Example: de.
        defer_nutriments (bool | Unset): Leave `nutriments` and `allergens` out of the answer and estimate them with a
            follow-up call to `POST /parse-recipe/nutriments`. Roughly halves the wait, because the first call then needs
            almost no reasoning budget. Clients that do not set it keep the single call. Default: False.
    """

    text: str
    target_language: str | Unset = UNSET
    defer_nutriments: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        text = self.text

        target_language = self.target_language

        defer_nutriments = self.defer_nutriments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "text": text,
            }
        )
        if target_language is not UNSET:
            field_dict["targetLanguage"] = target_language
        if defer_nutriments is not UNSET:
            field_dict["deferNutriments"] = defer_nutriments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        text = d.pop("text")

        target_language = d.pop("targetLanguage", UNSET)

        defer_nutriments = d.pop("deferNutriments", UNSET)

        parse_recipe_text_request_dto = cls(
            text=text,
            target_language=target_language,
            defer_nutriments=defer_nutriments,
        )

        parse_recipe_text_request_dto.additional_properties = d
        return parse_recipe_text_request_dto

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
