from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.allergen import Allergen
from ..models.volume_unit import VolumeUnit
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto
    from ..models.article_nutriments_dto import ArticleNutrimentsDto
    from ..models.barcode_affiliate_product_dto import BarcodeAffiliateProductDto
    from ..models.barcode_dto_language_specific import BarcodeDtoLanguageSpecific


T = TypeVar("T", bound="BarcodeDto")


@_attrs_define
class BarcodeDto:
    """
    Attributes:
        barcode (str):
        name (str):
        slug (str):
        category_uuid (str):
        content_volume (float):
        volume_unit (VolumeUnit):
        offers (list[BarcodeAffiliateProductDto]):
        indexable (bool): False when the page should render <meta name="robots" content="noindex">. Computed from GTIN
            validity, name length, image presence, and at least two of: brand, category, nutriments, tags or allergens
            (offers do not count).
        brand (str | Unset):
        language_specific (BarcodeDtoLanguageSpecific | Unset):
        author (str | Unset):
        image_url (str | Unset):
        additional_image_urls (list[str] | None | Unset): Additional product photo URLs, ordered. imageUrl is the
            primary photo.
        tags (list[str] | Unset):
        allergens (list[Allergen] | None | Unset): Allergens (EU 14) detected in the product. Best-effort guidance, not
            a legal declaration.
        nutriments (ArticleNutrimentsDto | Unset):
        complex_best_before_data (ArticleCatalogBestBeforeDatesDto | Unset):
    """

    barcode: str
    name: str
    slug: str
    category_uuid: str
    content_volume: float
    volume_unit: VolumeUnit
    offers: list[BarcodeAffiliateProductDto]
    indexable: bool
    brand: str | Unset = UNSET
    language_specific: BarcodeDtoLanguageSpecific | Unset = UNSET
    author: str | Unset = UNSET
    image_url: str | Unset = UNSET
    additional_image_urls: list[str] | None | Unset = UNSET
    tags: list[str] | Unset = UNSET
    allergens: list[Allergen] | None | Unset = UNSET
    nutriments: ArticleNutrimentsDto | Unset = UNSET
    complex_best_before_data: ArticleCatalogBestBeforeDatesDto | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        barcode = self.barcode

        name = self.name

        slug = self.slug

        category_uuid = self.category_uuid

        content_volume = self.content_volume

        volume_unit = self.volume_unit.value

        offers = []
        for offers_item_data in self.offers:
            offers_item = offers_item_data.to_dict()
            offers.append(offers_item)

        indexable = self.indexable

        brand = self.brand

        language_specific: dict[str, Any] | Unset = UNSET
        if not isinstance(self.language_specific, Unset):
            language_specific = self.language_specific.to_dict()

        author = self.author

        image_url = self.image_url

        additional_image_urls: list[str] | None | Unset
        if isinstance(self.additional_image_urls, Unset):
            additional_image_urls = UNSET
        elif isinstance(self.additional_image_urls, list):
            additional_image_urls = self.additional_image_urls

        else:
            additional_image_urls = self.additional_image_urls

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        allergens: list[str] | None | Unset
        if isinstance(self.allergens, Unset):
            allergens = UNSET
        elif isinstance(self.allergens, list):
            allergens = []
            for allergens_type_0_item_data in self.allergens:
                allergens_type_0_item = allergens_type_0_item_data.value
                allergens.append(allergens_type_0_item)

        else:
            allergens = self.allergens

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
                "slug": slug,
                "categoryUuid": category_uuid,
                "contentVolume": content_volume,
                "volumeUnit": volume_unit,
                "offers": offers,
                "indexable": indexable,
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
        if additional_image_urls is not UNSET:
            field_dict["additionalImageUrls"] = additional_image_urls
        if tags is not UNSET:
            field_dict["tags"] = tags
        if allergens is not UNSET:
            field_dict["allergens"] = allergens
        if nutriments is not UNSET:
            field_dict["nutriments"] = nutriments
        if complex_best_before_data is not UNSET:
            field_dict["complexBestBeforeData"] = complex_best_before_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto  # noqa: PLC0415
        from ..models.article_nutriments_dto import ArticleNutrimentsDto  # noqa: PLC0415
        from ..models.barcode_affiliate_product_dto import BarcodeAffiliateProductDto  # noqa: PLC0415
        from ..models.barcode_dto_language_specific import BarcodeDtoLanguageSpecific  # noqa: PLC0415

        d = dict(src_dict)
        barcode = d.pop("barcode")

        name = d.pop("name")

        slug = d.pop("slug")

        category_uuid = d.pop("categoryUuid")

        content_volume = d.pop("contentVolume")

        volume_unit = VolumeUnit(d.pop("volumeUnit"))

        offers = []
        _offers = d.pop("offers")
        for offers_item_data in _offers:
            offers_item = BarcodeAffiliateProductDto.from_dict(offers_item_data)

            offers.append(offers_item)

        indexable = d.pop("indexable")

        brand = d.pop("brand", UNSET)

        _language_specific = d.pop("languageSpecific", UNSET)
        language_specific: BarcodeDtoLanguageSpecific | Unset
        if isinstance(_language_specific, Unset) or _language_specific is None:
            language_specific = UNSET
        else:
            language_specific = BarcodeDtoLanguageSpecific.from_dict(_language_specific)

        author = d.pop("author", UNSET)

        image_url = d.pop("imageUrl", UNSET)

        def _parse_additional_image_urls(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                additional_image_urls_type_0 = cast(list[str], data)

                return additional_image_urls_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        additional_image_urls = _parse_additional_image_urls(d.pop("additionalImageUrls", UNSET))

        tags = cast(list[str], d.pop("tags", UNSET))

        def _parse_allergens(data: object) -> list[Allergen] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allergens_type_0 = []
                _allergens_type_0 = data
                for allergens_type_0_item_data in _allergens_type_0:
                    allergens_type_0_item = Allergen(allergens_type_0_item_data)

                    allergens_type_0.append(allergens_type_0_item)

                return allergens_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Allergen] | None | Unset, data)

        allergens = _parse_allergens(d.pop("allergens", UNSET))

        _nutriments = d.pop("nutriments", UNSET)
        nutriments: ArticleNutrimentsDto | Unset
        if isinstance(_nutriments, Unset) or _nutriments is None:
            nutriments = UNSET
        else:
            nutriments = ArticleNutrimentsDto.from_dict(_nutriments)

        _complex_best_before_data = d.pop("complexBestBeforeData", UNSET)
        complex_best_before_data: ArticleCatalogBestBeforeDatesDto | Unset
        if isinstance(_complex_best_before_data, Unset) or _complex_best_before_data is None:
            complex_best_before_data = UNSET
        else:
            complex_best_before_data = ArticleCatalogBestBeforeDatesDto.from_dict(_complex_best_before_data)

        barcode_dto = cls(
            barcode=barcode,
            name=name,
            slug=slug,
            category_uuid=category_uuid,
            content_volume=content_volume,
            volume_unit=volume_unit,
            offers=offers,
            indexable=indexable,
            brand=brand,
            language_specific=language_specific,
            author=author,
            image_url=image_url,
            additional_image_urls=additional_image_urls,
            tags=tags,
            allergens=allergens,
            nutriments=nutriments,
            complex_best_before_data=complex_best_before_data,
        )

        barcode_dto.additional_properties = d
        return barcode_dto

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
