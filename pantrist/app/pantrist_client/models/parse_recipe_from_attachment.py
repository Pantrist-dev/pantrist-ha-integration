from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ParseRecipeFromAttachment")


@_attrs_define
class ParseRecipeFromAttachment:
    """
    Attributes:
        base64 (str): The base64 encoded data of the attachment (image/document) Example:
            iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==.
        mime_type (str | Unset): The mime type of the attachment Default: 'image/jpeg'. Example: image/jpeg.
    """

    base64: str
    mime_type: str | Unset = "image/jpeg"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base64 = self.base64

        mime_type = self.mime_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "base64": base64,
            }
        )
        if mime_type is not UNSET:
            field_dict["mimeType"] = mime_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        base64 = d.pop("base64")

        mime_type = d.pop("mimeType", UNSET)

        parse_recipe_from_attachment = cls(
            base64=base64,
            mime_type=mime_type,
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
