from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.volume_unit import VolumeUnit
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto
    from ..models.article_nutriments_dto import ArticleNutrimentsDto
    from ..models.create_barcode_dto_language_specific import CreateBarcodeDtoLanguageSpecific


T = TypeVar("T", bound="CreateBarcodeDto")


@_attrs_define
class CreateBarcodeDto:
    """
    Attributes:
        barcode (str):
        name (str):
        category_uuid (str):
        content_volume (float):
        volume_unit (VolumeUnit):
        brand (str | Unset):
        language_specific (CreateBarcodeDtoLanguageSpecific | Unset):
        author (str | Unset):
        image_url (str | Unset):
        tags (list[str] | Unset):
        nutriments (ArticleNutrimentsDto | Unset):
        complex_best_before_data (ArticleCatalogBestBeforeDatesDto | Unset):
    """

    barcode: str
    name: str
    category_uuid: str
    content_volume: float
    volume_unit: VolumeUnit
    brand: str | Unset = UNSET
    language_specific: CreateBarcodeDtoLanguageSpecific | Unset = UNSET
    author: str | Unset = UNSET
    image_url: str | Unset = UNSET
    tags: list[str] | Unset = UNSET
    nutriments: ArticleNutrimentsDto | Unset = UNSET
    complex_best_before_data: ArticleCatalogBestBeforeDatesDto | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        barcode = self.barcode

        name = self.name

        category_uuid = self.category_uuid

        content_volume = self.content_volume

        volume_unit = self.volume_unit.value

        brand = self.brand

        language_specific: dict[str, Any] | Unset = UNSET
        if not isinstance(self.language_specific, Unset):
            language_specific = self.language_specific.to_dict()

        author = self.author

        image_url = self.image_url

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        nutriments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.nutriments, Unset):
            nutriments = self.nutriments.to_dict()

        complex_best_before_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.complex_best_before_data, Unset):
            complex_best_before_data = self.complex_best_before_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "barcode": barcode,
                "name": name,
                "categoryUuid": category_uuid,
                "contentVolume": content_volume,
                "volumeUnit": volume_unit,
            }
        )
        if brand is not UNSET:
            field_dict["brand"] = brand
        if language_specific is not UNSET:
            field_dict["languageSpecific"] = language_specific
        if author is not UNSET:
            field_dict["author"] = author
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if tags is not UNSET:
            field_dict["tags"] = tags
        if nutriments is not UNSET:
            field_dict["nutriments"] = nutriments
        if complex_best_before_data is not UNSET:
            field_dict["complexBestBeforeData"] = complex_best_before_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto
        from ..models.article_nutriments_dto import ArticleNutrimentsDto
        from ..models.create_barcode_dto_language_specific import CreateBarcodeDtoLanguageSpecific

        d = dict(src_dict)
        barcode = d.pop("barcode")

        name = d.pop("name")

        category_uuid = d.pop("categoryUuid")

        content_volume = d.pop("contentVolume")

        volume_unit = VolumeUnit(d.pop("volumeUnit"))

        brand = d.pop("brand", UNSET)

        _language_specific = d.pop("languageSpecific", UNSET)
        language_specific: CreateBarcodeDtoLanguageSpecific | Unset
        if isinstance(_language_specific, Unset):
            language_specific = UNSET
        else:
            language_specific = CreateBarcodeDtoLanguageSpecific.from_dict(_language_specific)

        author = d.pop("author", UNSET)

        image_url = d.pop("imageUrl", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _nutriments = d.pop("nutriments", UNSET)
        nutriments: ArticleNutrimentsDto | Unset
        if isinstance(_nutriments, Unset):
            nutriments = UNSET
        else:
            nutriments = ArticleNutrimentsDto.from_dict(_nutriments)

        _complex_best_before_data = d.pop("complexBestBeforeData", UNSET)
        complex_best_before_data: ArticleCatalogBestBeforeDatesDto | Unset
        if isinstance(_complex_best_before_data, Unset):
            complex_best_before_data = UNSET
        else:
            complex_best_before_data = ArticleCatalogBestBeforeDatesDto.from_dict(_complex_best_before_data)

        create_barcode_dto = cls(
            barcode=barcode,
            name=name,
            category_uuid=category_uuid,
            content_volume=content_volume,
            volume_unit=volume_unit,
            brand=brand,
            language_specific=language_specific,
            author=author,
            image_url=image_url,
            tags=tags,
            nutriments=nutriments,
            complex_best_before_data=complex_best_before_data,
        )

        create_barcode_dto.additional_properties = d
        return create_barcode_dto

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
