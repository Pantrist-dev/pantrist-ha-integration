from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.parse_recipe_request_dto_type import ParseRecipeRequestDtoType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ParseRecipeRequestDto")


@_attrs_define
class ParseRecipeRequestDto:
    """
    Attributes:
        url (str): The URL of the recipe to parse Example: https://www.example.com/recipe/123.
        type_ (ParseRecipeRequestDtoType | Unset): The type of parsing to perform Default:
            ParseRecipeRequestDtoType.NORMAL.
        target_language (str | Unset): Translate the parsed recipe into this language instead of preserving the source
            language. Accepts a BCP 47 tag (e.g. `de`, `en-US`, `pt-BR`). Only the human-readable fields are translated;
            unit codes, categories and allergens stay as their canonical identifiers. Omit to keep the source language
            (default). Only applies to the smart parser, since the basic parser does not run the recipe through a model.
            Example: de.
        defer_nutriments (bool | Unset): Leave `nutriments` and `allergens` out of the answer and estimate them with a
            follow-up call to `POST /parse-recipe/nutriments`. Roughly halves the wait, because the first call then needs
            almost no reasoning budget. Clients that do not set it keep the single call. Default: False.
    """

    url: str
    type_: ParseRecipeRequestDtoType | Unset = ParseRecipeRequestDtoType.NORMAL
    target_language: str | Unset = UNSET
    defer_nutriments: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        target_language = self.target_language

        defer_nutriments = self.defer_nutriments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_
        if target_language is not UNSET:
            field_dict["targetLanguage"] = target_language
        if defer_nutriments is not UNSET:
            field_dict["deferNutriments"] = defer_nutriments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        _type_ = d.pop("type", UNSET)
        type_: ParseRecipeRequestDtoType | Unset
        if isinstance(_type_, Unset) or _type_ is None or _type_ == "":
            type_ = UNSET
        else:
            type_ = ParseRecipeRequestDtoType(_type_)

        target_language = d.pop("targetLanguage", UNSET)

        defer_nutriments = d.pop("deferNutriments", UNSET)

        parse_recipe_request_dto = cls(
            url=url,
            type_=type_,
            target_language=target_language,
            defer_nutriments=defer_nutriments,
        )

        parse_recipe_request_dto.additional_properties = d
        return parse_recipe_request_dto

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
