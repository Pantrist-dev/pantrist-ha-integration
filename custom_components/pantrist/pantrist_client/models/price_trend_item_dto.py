from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.price_trend_point_dto import PriceTrendPointDto


T = TypeVar("T", bound="PriceTrendItemDto")


@_attrs_define
class PriceTrendItemDto:
    """
    Attributes:
        product_key (str): Stable identity. "bc:<barcode>" when a barcode exists, otherwise "nb:<name>|<brand>" (both
            normalized to lower-case + trimmed).
        name (str):
        purchase_count (float):
        last_purchase_date (str): Most recent purchase date (ISO string).
        last_unit_id (str):
        last_content_volume (float):
        market_uids (list[str]): Distinct supermarket UIDs this product has been purchased at.
        has_content_change (bool): True if at least one content-volume change has been detected for this product.
        recent_prices (list[PriceTrendPointDto]): The last purchases with a price (at most 8), oldest first: enough for
            a sparkline.
        brand (str | Unset):
        barcode (str | Unset):
        last_unit_price (float | Unset): Most recent unit price.
        last_price_per_content (float | Unset): Most recent price-per-content-unit.
        first_price (PriceTrendPointDto | Unset):
    """

    product_key: str
    name: str
    purchase_count: float
    last_purchase_date: str
    last_unit_id: str
    last_content_volume: float
    market_uids: list[str]
    has_content_change: bool
    recent_prices: list[PriceTrendPointDto]
    brand: str | Unset = UNSET
    barcode: str | Unset = UNSET
    last_unit_price: float | Unset = UNSET
    last_price_per_content: float | Unset = UNSET
    first_price: PriceTrendPointDto | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        product_key = self.product_key

        name = self.name

        purchase_count = self.purchase_count

        last_purchase_date = self.last_purchase_date

        last_unit_id = self.last_unit_id

        last_content_volume = self.last_content_volume

        market_uids = self.market_uids

        has_content_change = self.has_content_change

        recent_prices = []
        for recent_prices_item_data in self.recent_prices:
            recent_prices_item = recent_prices_item_data.to_dict()
            recent_prices.append(recent_prices_item)

        brand = self.brand

        barcode = self.barcode

        last_unit_price = self.last_unit_price

        last_price_per_content = self.last_price_per_content

        first_price: dict[str, Any] | Unset = UNSET
        if not isinstance(self.first_price, Unset):
            first_price = self.first_price.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "productKey": product_key,
                "name": name,
                "purchaseCount": purchase_count,
                "lastPurchaseDate": last_purchase_date,
                "lastUnitId": last_unit_id,
                "lastContentVolume": last_content_volume,
                "marketUids": market_uids,
                "hasContentChange": has_content_change,
                "recentPrices": recent_prices,
            }
        )
        if brand is not UNSET:
            field_dict["brand"] = brand
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if last_unit_price is not UNSET:
            field_dict["lastUnitPrice"] = last_unit_price
        if last_price_per_content is not UNSET:
            field_dict["lastPricePerContent"] = last_price_per_content
        if first_price is not UNSET:
            field_dict["firstPrice"] = first_price

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.price_trend_point_dto import PriceTrendPointDto  # noqa: PLC0415

        d = dict(src_dict)
        product_key = d.pop("productKey")

        name = d.pop("name")

        purchase_count = d.pop("purchaseCount")

        last_purchase_date = d.pop("lastPurchaseDate")

        last_unit_id = d.pop("lastUnitId")

        last_content_volume = d.pop("lastContentVolume")

        market_uids = cast(list[str], d.pop("marketUids"))

        has_content_change = d.pop("hasContentChange")

        recent_prices = []
        _recent_prices = d.pop("recentPrices")
        for recent_prices_item_data in _recent_prices:
            recent_prices_item = PriceTrendPointDto.from_dict(recent_prices_item_data)

            recent_prices.append(recent_prices_item)

        brand = d.pop("brand", UNSET)

        barcode = d.pop("barcode", UNSET)

        last_unit_price = d.pop("lastUnitPrice", UNSET)

        last_price_per_content = d.pop("lastPricePerContent", UNSET)

        _first_price = d.pop("firstPrice", UNSET)
        first_price: PriceTrendPointDto | Unset
        if isinstance(_first_price, Unset) or _first_price is None:
            first_price = UNSET
        else:
            first_price = PriceTrendPointDto.from_dict(_first_price)

        price_trend_item_dto = cls(
            product_key=product_key,
            name=name,
            purchase_count=purchase_count,
            last_purchase_date=last_purchase_date,
            last_unit_id=last_unit_id,
            last_content_volume=last_content_volume,
            market_uids=market_uids,
            has_content_change=has_content_change,
            recent_prices=recent_prices,
            brand=brand,
            barcode=barcode,
            last_unit_price=last_unit_price,
            last_price_per_content=last_price_per_content,
            first_price=first_price,
        )

        price_trend_item_dto.additional_properties = d
        return price_trend_item_dto

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
