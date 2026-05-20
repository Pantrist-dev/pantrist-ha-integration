from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_dto_complex_best_before_data import ArticleDtoComplexBestBeforeData
    from ..models.article_dto_nutriments import ArticleDtoNutriments
    from ..models.article_dto_price_per_market import ArticleDtoPricePerMarket
    from ..models.article_dto_supermarket_id import ArticleDtoSupermarketId
    from ..models.item_pantry_settings_dto import ItemPantrySettingsDto


T = TypeVar("T", bound="ArticleDto")


@_attrs_define
class ArticleDto:
    """
    Attributes:
        name (str):
        timestamp (float):
        category_uuid (str):
        content_volume (float):
        unit_id (str):
        amount (float):
        manage_minimum_amount (bool):
        minimum_amount (float):
        amount_to_buy (float):
        discount_per_unit_or_total (str):
        discount_type (str):
        pantry_settings (ItemPantrySettingsDto):
        uuid (str | Unset):
        brand (str | Unset):
        barcode (list[str] | str | Unset):
        notes (str | Unset):
        supermarket_id (ArticleDtoSupermarketId | Unset):
        disable_min_amount (bool | Unset):
        price (float | Unset):
        price_type (str | Unset):
        deposit (float | Unset):
        discount (float | Unset):
        coupon_name (str | Unset):
        coupon_expiration_date (str | Unset):
        image_url (str | Unset):
        purchase_date (str | Unset):
        last_inventory_date (str | Unset):
        tags (list[str] | Unset):
        nutriments (ArticleDtoNutriments | Unset):
        complex_best_before_data (ArticleDtoComplexBestBeforeData | Unset):
        generic_price_from_catalog (float | Unset):
        price_per_market (ArticleDtoPricePerMarket | Unset):
    """

    name: str
    timestamp: float
    category_uuid: str
    content_volume: float
    unit_id: str
    amount: float
    manage_minimum_amount: bool
    minimum_amount: float
    amount_to_buy: float
    discount_per_unit_or_total: str
    discount_type: str
    pantry_settings: ItemPantrySettingsDto
    uuid: str | Unset = UNSET
    brand: str | Unset = UNSET
    barcode: list[str] | str | Unset = UNSET
    notes: str | Unset = UNSET
    supermarket_id: ArticleDtoSupermarketId | Unset = UNSET
    disable_min_amount: bool | Unset = UNSET
    price: float | Unset = UNSET
    price_type: str | Unset = UNSET
    deposit: float | Unset = UNSET
    discount: float | Unset = UNSET
    coupon_name: str | Unset = UNSET
    coupon_expiration_date: str | Unset = UNSET
    image_url: str | Unset = UNSET
    purchase_date: str | Unset = UNSET
    last_inventory_date: str | Unset = UNSET
    tags: list[str] | Unset = UNSET
    nutriments: ArticleDtoNutriments | Unset = UNSET
    complex_best_before_data: ArticleDtoComplexBestBeforeData | Unset = UNSET
    generic_price_from_catalog: float | Unset = UNSET
    price_per_market: ArticleDtoPricePerMarket | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        timestamp = self.timestamp

        category_uuid = self.category_uuid

        content_volume = self.content_volume

        unit_id = self.unit_id

        amount = self.amount

        manage_minimum_amount = self.manage_minimum_amount

        minimum_amount = self.minimum_amount

        amount_to_buy = self.amount_to_buy

        discount_per_unit_or_total = self.discount_per_unit_or_total

        discount_type = self.discount_type

        pantry_settings = self.pantry_settings.to_dict()

        uuid = self.uuid

        brand = self.brand

        barcode: list[str] | str | Unset
        if isinstance(self.barcode, Unset):
            barcode = UNSET
        elif isinstance(self.barcode, list):
            barcode = self.barcode

        else:
            barcode = self.barcode

        notes = self.notes

        supermarket_id: dict[str, Any] | Unset = UNSET
        if not isinstance(self.supermarket_id, Unset):
            supermarket_id = self.supermarket_id.to_dict()

        disable_min_amount = self.disable_min_amount

        price = self.price

        price_type = self.price_type

        deposit = self.deposit

        discount = self.discount

        coupon_name = self.coupon_name

        coupon_expiration_date = self.coupon_expiration_date

        image_url = self.image_url

        purchase_date = self.purchase_date

        last_inventory_date = self.last_inventory_date

        tags: list[str] | Unset = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags

        nutriments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.nutriments, Unset):
            nutriments = self.nutriments.to_dict()

        complex_best_before_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.complex_best_before_data, Unset):
            complex_best_before_data = self.complex_best_before_data.to_dict()

        generic_price_from_catalog = self.generic_price_from_catalog

        price_per_market: dict[str, Any] | Unset = UNSET
        if not isinstance(self.price_per_market, Unset):
            price_per_market = self.price_per_market.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "timestamp": timestamp,
                "categoryUuid": category_uuid,
                "contentVolume": content_volume,
                "unitId": unit_id,
                "amount": amount,
                "manageMinimumAmount": manage_minimum_amount,
                "minimumAmount": minimum_amount,
                "amountToBuy": amount_to_buy,
                "discountPerUnitOrTotal": discount_per_unit_or_total,
                "discountType": discount_type,
                "pantrySettings": pantry_settings,
            }
        )
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if brand is not UNSET:
            field_dict["brand"] = brand
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if notes is not UNSET:
            field_dict["notes"] = notes
        if supermarket_id is not UNSET:
            field_dict["supermarketId"] = supermarket_id
        if disable_min_amount is not UNSET:
            field_dict["disableMinAmount"] = disable_min_amount
        if price is not UNSET:
            field_dict["price"] = price
        if price_type is not UNSET:
            field_dict["priceType"] = price_type
        if deposit is not UNSET:
            field_dict["deposit"] = deposit
        if discount is not UNSET:
            field_dict["discount"] = discount
        if coupon_name is not UNSET:
            field_dict["couponName"] = coupon_name
        if coupon_expiration_date is not UNSET:
            field_dict["couponExpirationDate"] = coupon_expiration_date
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if purchase_date is not UNSET:
            field_dict["purchaseDate"] = purchase_date
        if last_inventory_date is not UNSET:
            field_dict["lastInventoryDate"] = last_inventory_date
        if tags is not UNSET:
            field_dict["tags"] = tags
        if nutriments is not UNSET:
            field_dict["nutriments"] = nutriments
        if complex_best_before_data is not UNSET:
            field_dict["complexBestBeforeData"] = complex_best_before_data
        if generic_price_from_catalog is not UNSET:
            field_dict["genericPriceFromCatalog"] = generic_price_from_catalog
        if price_per_market is not UNSET:
            field_dict["pricePerMarket"] = price_per_market

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_dto_complex_best_before_data import ArticleDtoComplexBestBeforeData
        from ..models.article_dto_nutriments import ArticleDtoNutriments
        from ..models.article_dto_price_per_market import ArticleDtoPricePerMarket
        from ..models.article_dto_supermarket_id import ArticleDtoSupermarketId
        from ..models.item_pantry_settings_dto import ItemPantrySettingsDto

        d = dict(src_dict)
        name = d.pop("name")

        timestamp = d.pop("timestamp")

        category_uuid = d.pop("categoryUuid")

        content_volume = d.pop("contentVolume")

        unit_id = d.pop("unitId")

        amount = d.pop("amount")

        manage_minimum_amount = d.pop("manageMinimumAmount")

        minimum_amount = d.pop("minimumAmount")

        amount_to_buy = d.pop("amountToBuy")

        discount_per_unit_or_total = d.pop("discountPerUnitOrTotal")

        discount_type = d.pop("discountType")

        pantry_settings = ItemPantrySettingsDto.from_dict(d.pop("pantrySettings"))

        uuid = d.pop("uuid", UNSET)

        brand = d.pop("brand", UNSET)

        def _parse_barcode(data: object) -> list[str] | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                barcode_type_1 = cast(list[str], data)

                return barcode_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | str | Unset, data)

        barcode = _parse_barcode(d.pop("barcode", UNSET))

        notes = d.pop("notes", UNSET)

        _supermarket_id = d.pop("supermarketId", UNSET)
        supermarket_id: ArticleDtoSupermarketId | Unset
        if isinstance(_supermarket_id, Unset):
            supermarket_id = UNSET
        else:
            supermarket_id = ArticleDtoSupermarketId.from_dict(_supermarket_id)

        disable_min_amount = d.pop("disableMinAmount", UNSET)

        price = d.pop("price", UNSET)

        price_type = d.pop("priceType", UNSET)

        deposit = d.pop("deposit", UNSET)

        discount = d.pop("discount", UNSET)

        coupon_name = d.pop("couponName", UNSET)

        coupon_expiration_date = d.pop("couponExpirationDate", UNSET)

        image_url = d.pop("imageUrl", UNSET)

        purchase_date = d.pop("purchaseDate", UNSET)

        last_inventory_date = d.pop("lastInventoryDate", UNSET)

        tags = cast(list[str], d.pop("tags", UNSET))

        _nutriments = d.pop("nutriments", UNSET)
        nutriments: ArticleDtoNutriments | Unset
        if isinstance(_nutriments, Unset):
            nutriments = UNSET
        else:
            nutriments = ArticleDtoNutriments.from_dict(_nutriments)

        _complex_best_before_data = d.pop("complexBestBeforeData", UNSET)
        complex_best_before_data: ArticleDtoComplexBestBeforeData | Unset
        if isinstance(_complex_best_before_data, Unset):
            complex_best_before_data = UNSET
        else:
            complex_best_before_data = ArticleDtoComplexBestBeforeData.from_dict(_complex_best_before_data)

        generic_price_from_catalog = d.pop("genericPriceFromCatalog", UNSET)

        _price_per_market = d.pop("pricePerMarket", UNSET)
        price_per_market: ArticleDtoPricePerMarket | Unset
        if isinstance(_price_per_market, Unset):
            price_per_market = UNSET
        else:
            price_per_market = ArticleDtoPricePerMarket.from_dict(_price_per_market)

        article_dto = cls(
            name=name,
            timestamp=timestamp,
            category_uuid=category_uuid,
            content_volume=content_volume,
            unit_id=unit_id,
            amount=amount,
            manage_minimum_amount=manage_minimum_amount,
            minimum_amount=minimum_amount,
            amount_to_buy=amount_to_buy,
            discount_per_unit_or_total=discount_per_unit_or_total,
            discount_type=discount_type,
            pantry_settings=pantry_settings,
            uuid=uuid,
            brand=brand,
            barcode=barcode,
            notes=notes,
            supermarket_id=supermarket_id,
            disable_min_amount=disable_min_amount,
            price=price,
            price_type=price_type,
            deposit=deposit,
            discount=discount,
            coupon_name=coupon_name,
            coupon_expiration_date=coupon_expiration_date,
            image_url=image_url,
            purchase_date=purchase_date,
            last_inventory_date=last_inventory_date,
            tags=tags,
            nutriments=nutriments,
            complex_best_before_data=complex_best_before_data,
            generic_price_from_catalog=generic_price_from_catalog,
            price_per_market=price_per_market,
        )

        article_dto.additional_properties = d
        return article_dto

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
