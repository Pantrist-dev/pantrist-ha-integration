from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parse_recipe_collection_attachment_dto import ParseRecipeCollectionAttachmentDto


T = TypeVar("T", bound="ParseRecipeCollectionRequestDto")


@_attrs_define
class ParseRecipeCollectionRequestDto:
    """
    Attributes:
        url (str | Unset): URL of a social post or recipe page. A carousel with several recipes yields several results.
            Example: https://www.instagram.com/p/ABC123/.
        attachments (list[ParseRecipeCollectionAttachmentDto] | Unset): Photos or PDFs. Images are grouped by recipe
            automatically: pages of one recipe become one result, distinct recipes become distinct results.
        target_language (str | Unset): Translate the parsed recipes into this language instead of preserving the source
            language. BCP 47 tag. Example: de.
        defer_nutriments (bool | Unset): Leave `nutriments` and `allergens` out of the answer and estimate them with a
            follow-up call to `POST /parse-recipe/nutriments`. Roughly halves the wait, because the first call then needs
            almost no reasoning budget. Clients that do not set it keep the single call. Default: False.
    """

    url: str | Unset = UNSET
    attachments: list[ParseRecipeCollectionAttachmentDto] | Unset = UNSET
    target_language: str | Unset = UNSET
    defer_nutriments: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        attachments: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.attachments, Unset):
            attachments = []
            for attachments_item_data in self.attachments:
                attachments_item = attachments_item_data.to_dict()
                attachments.append(attachments_item)

        target_language = self.target_language

        defer_nutriments = self.defer_nutriments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if attachments is not UNSET:
            field_dict["attachments"] = attachments
        if target_language is not UNSET:
            field_dict["targetLanguage"] = target_language
        if defer_nutriments is not UNSET:
            field_dict["deferNutriments"] = defer_nutriments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.parse_recipe_collection_attachment_dto import ParseRecipeCollectionAttachmentDto  # noqa: PLC0415

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _attachments = d.pop("attachments", UNSET)
        attachments: list[ParseRecipeCollectionAttachmentDto] | Unset = UNSET
        if _attachments is not UNSET:
            attachments = []
            for attachments_item_data in _attachments:
                attachments_item = ParseRecipeCollectionAttachmentDto.from_dict(attachments_item_data)

                attachments.append(attachments_item)

        target_language = d.pop("targetLanguage", UNSET)

        defer_nutriments = d.pop("deferNutriments", UNSET)

        parse_recipe_collection_request_dto = cls(
            url=url,
            attachments=attachments,
            target_language=target_language,
            defer_nutriments=defer_nutriments,
        )

        parse_recipe_collection_request_dto.additional_properties = d
        return parse_recipe_collection_request_dto

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
