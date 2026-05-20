from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BarcodeSummaryDto")


@_attrs_define
class BarcodeSummaryDto:
    """
    Attributes:
        ean (str): EAN / barcode number
        slug (str): URL slug
        name (str):
        brand (str | Unset):
        image (str | Unset):
    """

    ean: str
    slug: str
    name: str
    brand: str | Unset = UNSET
    image: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ean = self.ean

        slug = self.slug

        name = self.name

        brand = self.brand

        image = self.image

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ean": ean,
                "slug": slug,
                "name": name,
            }
        )
        if brand is not UNSET:
            field_dict["brand"] = brand
        if image is not UNSET:
            field_dict["image"] = image

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ean = d.pop("ean")

        slug = d.pop("slug")

        name = d.pop("name")

        brand = d.pop("brand", UNSET)

        image = d.pop("image", UNSET)

        barcode_summary_dto = cls(
            ean=ean,
            slug=slug,
            name=name,
            brand=brand,
            image=image,
        )

        barcode_summary_dto.additional_properties = d
        return barcode_summary_dto

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
