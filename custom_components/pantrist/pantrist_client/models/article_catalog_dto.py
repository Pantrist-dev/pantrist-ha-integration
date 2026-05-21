from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto
    from ..models.article_catalog_dto_price_per_market_type_0 import ArticleCatalogDtoPricePerMarketType0
    from ..models.article_nutriments_dto import ArticleNutrimentsDto
    from ..models.price_with_date_dto import PriceWithDateDto


T = TypeVar("T", bound="ArticleCatalogDto")


@_attrs_define
class ArticleCatalogDto:
    """
    Attributes:
        uuid (str):
        name (str):
        category_uuid (str):
        content_volume (float):
        brand (None | str | Unset):
        unit_id (None | str | Unset):
        barcode (list[str] | None | Unset):
        supermarket_id (list[str] | None | Unset):
        tags (list[str] | None | Unset):
        favourite (bool | None | Unset):
        deposit (float | None | Unset):
        image_url (None | str | Unset):
        predefined_pantry (None | str | Unset):
        notes (None | str | Unset):
        default_best_before_days (float | None | Unset):
        manage_minimum_amount (bool | None | Unset):
        minimum_amount (float | None | Unset):
        amount_to_buy (float | None | Unset):
        price (PriceWithDateDto | Unset):
        price_per_market (ArticleCatalogDtoPricePerMarketType0 | None | Unset):
        nutriments (ArticleNutrimentsDto | Unset):
        complex_best_before_data (ArticleCatalogBestBeforeDatesDto | Unset):
    """

    uuid: str
    name: str
    category_uuid: str
    content_volume: float
    brand: None | str | Unset = UNSET
    unit_id: None | str | Unset = UNSET
    barcode: list[str] | None | Unset = UNSET
    supermarket_id: list[str] | None | Unset = UNSET
    tags: list[str] | None | Unset = UNSET
    favourite: bool | None | Unset = UNSET
    deposit: float | None | Unset = UNSET
    image_url: None | str | Unset = UNSET
    predefined_pantry: None | str | Unset = UNSET
    notes: None | str | Unset = UNSET
    default_best_before_days: float | None | Unset = UNSET
    manage_minimum_amount: bool | None | Unset = UNSET
    minimum_amount: float | None | Unset = UNSET
    amount_to_buy: float | None | Unset = UNSET
    price: PriceWithDateDto | Unset = UNSET
    price_per_market: ArticleCatalogDtoPricePerMarketType0 | None | Unset = UNSET
    nutriments: ArticleNutrimentsDto | Unset = UNSET
    complex_best_before_data: ArticleCatalogBestBeforeDatesDto | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.article_catalog_dto_price_per_market_type_0 import ArticleCatalogDtoPricePerMarketType0

        uuid = self.uuid

        name = self.name

        category_uuid = self.category_uuid

        content_volume = self.content_volume

        brand: None | str | Unset
        if isinstance(self.brand, Unset):
            brand = UNSET
        else:
            brand = self.brand

        unit_id: None | str | Unset
        if isinstance(self.unit_id, Unset):
            unit_id = UNSET
        else:
            unit_id = self.unit_id

        barcode: list[str] | None | Unset
        if isinstance(self.barcode, Unset):
            barcode = UNSET
        elif isinstance(self.barcode, list):
            barcode = self.barcode

        else:
            barcode = self.barcode

        supermarket_id: list[str] | None | Unset
        if isinstance(self.supermarket_id, Unset):
            supermarket_id = UNSET
        elif isinstance(self.supermarket_id, list):
            supermarket_id = self.supermarket_id

        else:
            supermarket_id = self.supermarket_id

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        favourite: bool | None | Unset
        if isinstance(self.favourite, Unset):
            favourite = UNSET
        else:
            favourite = self.favourite

        deposit: float | None | Unset
        if isinstance(self.deposit, Unset):
            deposit = UNSET
        else:
            deposit = self.deposit

        image_url: None | str | Unset
        if isinstance(self.image_url, Unset):
            image_url = UNSET
        else:
            image_url = self.image_url

        predefined_pantry: None | str | Unset
        if isinstance(self.predefined_pantry, Unset):
            predefined_pantry = UNSET
        else:
            predefined_pantry = self.predefined_pantry

        notes: None | str | Unset
        if isinstance(self.notes, Unset):
            notes = UNSET
        else:
            notes = self.notes

        default_best_before_days: float | None | Unset
        if isinstance(self.default_best_before_days, Unset):
            default_best_before_days = UNSET
        else:
            default_best_before_days = self.default_best_before_days

        manage_minimum_amount: bool | None | Unset
        if isinstance(self.manage_minimum_amount, Unset):
            manage_minimum_amount = UNSET
        else:
            manage_minimum_amount = self.manage_minimum_amount

        minimum_amount: float | None | Unset
        if isinstance(self.minimum_amount, Unset):
            minimum_amount = UNSET
        else:
            minimum_amount = self.minimum_amount

        amount_to_buy: float | None | Unset
        if isinstance(self.amount_to_buy, Unset):
            amount_to_buy = UNSET
        else:
            amount_to_buy = self.amount_to_buy

        price: dict[str, Any] | Unset = UNSET
        if not isinstance(self.price, Unset):
            price = self.price.to_dict()

        price_per_market: dict[str, Any] | None | Unset
        if isinstance(self.price_per_market, Unset):
            price_per_market = UNSET
        elif isinstance(self.price_per_market, ArticleCatalogDtoPricePerMarketType0):
            price_per_market = self.price_per_market.to_dict()
        else:
            price_per_market = self.price_per_market

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
                "uuid": uuid,
                "name": name,
                "categoryUuid": category_uuid,
                "contentVolume": content_volume,
            }
        )
        if brand is not UNSET:
            field_dict["brand"] = brand
        if unit_id is not UNSET:
            field_dict["unitId"] = unit_id
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if supermarket_id is not UNSET:
            field_dict["supermarketId"] = supermarket_id
        if tags is not UNSET:
            field_dict["tags"] = tags
        if favourite is not UNSET:
            field_dict["favourite"] = favourite
        if deposit is not UNSET:
            field_dict["deposit"] = deposit
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if predefined_pantry is not UNSET:
            field_dict["predefinedPantry"] = predefined_pantry
        if notes is not UNSET:
            field_dict["notes"] = notes
        if default_best_before_days is not UNSET:
            field_dict["defaultBestBeforeDays"] = default_best_before_days
        if manage_minimum_amount is not UNSET:
            field_dict["manageMinimumAmount"] = manage_minimum_amount
        if minimum_amount is not UNSET:
            field_dict["minimumAmount"] = minimum_amount
        if amount_to_buy is not UNSET:
            field_dict["amountToBuy"] = amount_to_buy
        if price is not UNSET:
            field_dict["price"] = price
        if price_per_market is not UNSET:
            field_dict["pricePerMarket"] = price_per_market
        if nutriments is not UNSET:
            field_dict["nutriments"] = nutriments
        if complex_best_before_data is not UNSET:
            field_dict["complexBestBeforeData"] = complex_best_before_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto
        from ..models.article_catalog_dto_price_per_market_type_0 import ArticleCatalogDtoPricePerMarketType0
        from ..models.article_nutriments_dto import ArticleNutrimentsDto
        from ..models.price_with_date_dto import PriceWithDateDto

        d = dict(src_dict)
        uuid = d.pop("uuid")

        name = d.pop("name")

        category_uuid = d.pop("categoryUuid")

        content_volume = d.pop("contentVolume")

        def _parse_brand(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        brand = _parse_brand(d.pop("brand", UNSET))

        def _parse_unit_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit_id = _parse_unit_id(d.pop("unitId", UNSET))

        def _parse_barcode(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                barcode_type_0 = cast(list[str], data)

                return barcode_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        barcode = _parse_barcode(d.pop("barcode", UNSET))

        def _parse_supermarket_id(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                supermarket_id_type_0 = cast(list[str], data)

                return supermarket_id_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        supermarket_id = _parse_supermarket_id(d.pop("supermarketId", UNSET))

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_favourite(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        favourite = _parse_favourite(d.pop("favourite", UNSET))

        def _parse_deposit(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        deposit = _parse_deposit(d.pop("deposit", UNSET))

        def _parse_image_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        image_url = _parse_image_url(d.pop("imageUrl", UNSET))

        def _parse_predefined_pantry(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        predefined_pantry = _parse_predefined_pantry(d.pop("predefinedPantry", UNSET))

        def _parse_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        notes = _parse_notes(d.pop("notes", UNSET))

        def _parse_default_best_before_days(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        default_best_before_days = _parse_default_best_before_days(d.pop("defaultBestBeforeDays", UNSET))

        def _parse_manage_minimum_amount(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        manage_minimum_amount = _parse_manage_minimum_amount(d.pop("manageMinimumAmount", UNSET))

        def _parse_minimum_amount(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        minimum_amount = _parse_minimum_amount(d.pop("minimumAmount", UNSET))

        def _parse_amount_to_buy(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        amount_to_buy = _parse_amount_to_buy(d.pop("amountToBuy", UNSET))

        _price = d.pop("price", UNSET)
        price: PriceWithDateDto | Unset
        if isinstance(_price, Unset) or _price is None:
            price = UNSET
        else:
            price = PriceWithDateDto.from_dict(_price)

        def _parse_price_per_market(data: object) -> ArticleCatalogDtoPricePerMarketType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                price_per_market_type_0 = ArticleCatalogDtoPricePerMarketType0.from_dict(data)

                return price_per_market_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ArticleCatalogDtoPricePerMarketType0 | None | Unset, data)

        price_per_market = _parse_price_per_market(d.pop("pricePerMarket", UNSET))

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

        article_catalog_dto = cls(
            uuid=uuid,
            name=name,
            category_uuid=category_uuid,
            content_volume=content_volume,
            brand=brand,
            unit_id=unit_id,
            barcode=barcode,
            supermarket_id=supermarket_id,
            tags=tags,
            favourite=favourite,
            deposit=deposit,
            image_url=image_url,
            predefined_pantry=predefined_pantry,
            notes=notes,
            default_best_before_days=default_best_before_days,
            manage_minimum_amount=manage_minimum_amount,
            minimum_amount=minimum_amount,
            amount_to_buy=amount_to_buy,
            price=price,
            price_per_market=price_per_market,
            nutriments=nutriments,
            complex_best_before_data=complex_best_before_data,
        )

        article_catalog_dto.additional_properties = d
        return article_catalog_dto

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
