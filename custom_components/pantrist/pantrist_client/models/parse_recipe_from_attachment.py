from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.parse_recipe_additional_attachment import ParseRecipeAdditionalAttachment


T = TypeVar("T", bound="ParseRecipeFromAttachment")


@_attrs_define
class ParseRecipeFromAttachment:
    """
    Attributes:
        base64 (str): The base64 encoded data of the attachment (image/document) Example:
            iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==.
        mime_type (str | Unset): The mime type of the attachment Default: 'image/jpeg'. Example: image/jpeg.
        additional_attachments (list[ParseRecipeAdditionalAttachment] | Unset): Optional additional attachments parsed
            together with the primary one. Used when one recipe spans multiple photos so the AI sees them as a single unit.
        target_language (str | Unset): Translate the parsed recipe into this language instead of preserving the source
            language. Accepts a BCP 47 tag (e.g. `de`, `en-US`, `pt-BR`). Only the human-readable fields are translated;
            unit codes, categories and allergens stay as their canonical identifiers. Omit to keep the source language
            (default). Example: de.
        defer_nutriments (bool | Unset): Leave `nutriments` and `allergens` out of the answer and estimate them with a
            follow-up call to `POST /parse-recipe/nutriments`. Roughly halves the wait, because the first call then needs
            almost no reasoning budget. Clients that do not set it keep the single call. Default: False.
    """

    base64: str
    mime_type: str | Unset = "image/jpeg"
    additional_attachments: list[ParseRecipeAdditionalAttachment] | Unset = UNSET
    target_language: str | Unset = UNSET
    defer_nutriments: bool | Unset = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base64 = self.base64

        mime_type = self.mime_type

        additional_attachments: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.additional_attachments, Unset):
            additional_attachments = []
            for additional_attachments_item_data in self.additional_attachments:
                additional_attachments_item = additional_attachments_item_data.to_dict()
                additional_attachments.append(additional_attachments_item)

        target_language = self.target_language

        defer_nutriments = self.defer_nutriments

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "base64": base64,
            }
        )
        if mime_type is not UNSET:
            field_dict["mimeType"] = mime_type
        if additional_attachments is not UNSET:
            field_dict["additionalAttachments"] = additional_attachments
        if target_language is not UNSET:
            field_dict["targetLanguage"] = target_language
        if defer_nutriments is not UNSET:
            field_dict["deferNutriments"] = defer_nutriments

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.parse_recipe_additional_attachment import ParseRecipeAdditionalAttachment  # noqa: PLC0415

        d = dict(src_dict)
        base64 = d.pop("base64")

        mime_type = d.pop("mimeType", UNSET)

        _additional_attachments = d.pop("additionalAttachments", UNSET)
        additional_attachments: list[ParseRecipeAdditionalAttachment] | Unset = UNSET
        if _additional_attachments is not UNSET:
            additional_attachments = []
            for additional_attachments_item_data in _additional_attachments:
                additional_attachments_item = ParseRecipeAdditionalAttachment.from_dict(
                    additional_attachments_item_data
                )

                additional_attachments.append(additional_attachments_item)

        target_language = d.pop("targetLanguage", UNSET)

        defer_nutriments = d.pop("deferNutriments", UNSET)

        parse_recipe_from_attachment = cls(
            base64=base64,
            mime_type=mime_type,
            additional_attachments=additional_attachments,
            target_language=target_language,
            defer_nutriments=defer_nutriments,
        )

        parse_recipe_from_attachment.additional_properties = d
        return parse_recipe_from_attachment

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
