from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.volume_unit import VolumeUnit
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto
    from ..models.article_nutriments_dto import ArticleNutrimentsDto
    from ..models.barcode_affiliate_product_dto import BarcodeAffiliateProductDto
    from ..models.barcode_page_dto_name_by_language import BarcodePageDtoNameByLanguage
    from ..models.barcode_summary_dto import BarcodeSummaryDto


T = TypeVar("T", bound="BarcodePageDto")


@_attrs_define
class BarcodePageDto:
    """
    Attributes:
        ean (str): EAN / barcode number
        slug (str): URL slug
        name (str): Default product name (matches the row written by the import pipeline).
        offers (list[BarcodeAffiliateProductDto]):
        related_barcodes (list[BarcodeSummaryDto]):
        updated_at (datetime.datetime):
        created_at (datetime.datetime):
        indexable (bool): False when the page should render <meta name="robots" content="noindex">.
        name_by_language (BarcodePageDtoNameByLanguage | Unset): Language-specific name overrides keyed by IETF language
            tag (de-DE, en-US, ...).
        brand (str | Unset):
        category_uuid (str | Unset): Raw category UUID. The frontend resolves name/slug from its local category list.
        image (str | Unset):
        images (list[str] | Unset): Additional product images if available.
        content_volume (float | Unset):
        volume_unit (VolumeUnit | Unset): Unit of the content. Besides the enum it's possible that custom IDs are used
            here
        nutriments (ArticleNutrimentsDto | Unset):
        complex_best_before_data (ArticleCatalogBestBeforeDatesDto | Unset):
        tags (list[str] | Unset):
    """

    ean: str
    slug: str
    name: str
    offers: list[BarcodeAffiliateProductDto]
    related_barcodes: list[BarcodeSummaryDto]
    updated_at: datetime.datetime
    created_at: datetime.datetime
    indexable: bool
    name_by_language: BarcodePageDtoNameByLanguage | Unset = UNSET
    brand: str | Unset = UNSET
    category_uuid: str | Unset = UNSET
    image: str | Unset = UNSET
    images: list[str] | Unset = UNSET
    content_volume: float | Unset = UNSET
    volume_unit: VolumeUnit | Unset = UNSET
    nutriments: ArticleNutrimentsDto | Unset = UNSET
    complex_best_before_data: ArticleCatalogBestBeforeDatesDto | Unset = UNSET
    tags: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ean = self.ean

        slug = self.slug

        name = self.name

        offers = []
        for offers_item_data in self.offers:
            offers_item = offers_item_data.to_dict()
            offers.append(offers_item)

        related_barcodes = []
        for related_barcodes_item_data in self.related_barcodes:
            related_barcodes_item = related_barcodes_item_data.to_dict()
            related_barcodes.append(related_barcodes_item)

        updated_at = self.updated_at.isoformat()

        created_at = self.created_at.isoformat()

        indexable = self.indexable

        name_by_language: dict[str, Any] | Unset = UNSET
        if not isinstance(self.name_by_language, Unset):
            name_by_language = self.name_by_language.to_dict()

        brand = self.brand

        category_uuid = self.category_uuid

        image = self.image

        images: list[str] | Unset = UNSET
        if not isinstance(self.images, Unset):
            images = self.images

        content_volume = self.content_volume

        volume_unit: str | Unset = UNSET
        if not isinstance(self.volume_unit, Unset):
            volume_unit = self.volume_unit.value

        nutriments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.nutriments, Unset):
            nutriments = self.nutriments.to_dict()

        complex_best_before_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.complex_best_before_data, Unset):
            complex_best_before_data = self.complex_best_before_data.to_dict()

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ean": ean,
                "slug": slug,
                "name": name,
                "offers": offers,
                "relatedBarcodes": related_barcodes,
                "updatedAt": updated_at,
                "createdAt": created_at,
                "indexable": indexable,
            }
        )
        if name_by_language is not UNSET:
            field_dict["nameByLanguage"] = name_by_language
        if brand is not UNSET:
            field_dict["brand"] = brand
        if category_uuid is not UNSET:
            field_dict["categoryUuid"] = category_uuid
        if image is not UNSET:
            field_dict["image"] = image
        if images is not UNSET:
            field_dict["images"] = images
        if content_volume is not UNSET:
            field_dict["contentVolume"] = content_volume
        if volume_unit is not UNSET:
            field_dict["volumeUnit"] = volume_unit
        if nutriments is not UNSET:
            field_dict["nutriments"] = nutriments
        if complex_best_before_data is not UNSET:
            field_dict["complexBestBeforeData"] = complex_best_before_data
        if tags is not UNSET:
            field_dict["tags"] = tags

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto
        from ..models.article_nutriments_dto import ArticleNutrimentsDto
        from ..models.barcode_affiliate_product_dto import BarcodeAffiliateProductDto
        from ..models.barcode_page_dto_name_by_language import BarcodePageDtoNameByLanguage
        from ..models.barcode_summary_dto import BarcodeSummaryDto

        d = dict(src_dict)
        ean = d.pop("ean")

        slug = d.pop("slug")

        name = d.pop("name")

        offers = []
        _offers = d.pop("offers")
        for offers_item_data in _offers:
            offers_item = BarcodeAffiliateProductDto.from_dict(offers_item_data)

            offers.append(offers_item)

        related_barcodes = []
        _related_barcodes = d.pop("relatedBarcodes")
        for related_barcodes_item_data in _related_barcodes:
            related_barcodes_item = BarcodeSummaryDto.from_dict(related_barcodes_item_data)

            related_barcodes.append(related_barcodes_item)

        updated_at = isoparse(d.pop("updatedAt"))

        created_at = isoparse(d.pop("createdAt"))

        indexable = d.pop("indexable")

        _name_by_language = d.pop("nameByLanguage", UNSET)
        name_by_language: BarcodePageDtoNameByLanguage | Unset
        if isinstance(_name_by_language, Unset):
            name_by_language = UNSET
        else:
            name_by_language = BarcodePageDtoNameByLanguage.from_dict(_name_by_language)

        brand = d.pop("brand", UNSET)

        category_uuid = d.pop("categoryUuid", UNSET)

        image = d.pop("image", UNSET)

        images = cast(list[str], d.pop("images", UNSET))

        content_volume = d.pop("contentVolume", UNSET)

        _volume_unit = d.pop("volumeUnit", UNSET)
        volume_unit: VolumeUnit | Unset
        if isinstance(_volume_unit, Unset):
            volume_unit = UNSET
        else:
            volume_unit = VolumeUnit(_volume_unit)

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

        tags = cast(list[str], d.pop("tags", UNSET))

        barcode_page_dto = cls(
            ean=ean,
            slug=slug,
            name=name,
            offers=offers,
            related_barcodes=related_barcodes,
            updated_at=updated_at,
            created_at=created_at,
            indexable=indexable,
            name_by_language=name_by_language,
            brand=brand,
            category_uuid=category_uuid,
            image=image,
            images=images,
            content_volume=content_volume,
            volume_unit=volume_unit,
            nutriments=nutriments,
            complex_best_before_data=complex_best_before_data,
            tags=tags,
        )

        barcode_page_dto.additional_properties = d
        return barcode_page_dto

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
