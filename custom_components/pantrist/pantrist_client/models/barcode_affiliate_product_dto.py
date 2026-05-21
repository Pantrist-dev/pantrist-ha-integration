from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="BarcodeAffiliateProductDto")


@_attrs_define
class BarcodeAffiliateProductDto:
    """
    Attributes:
        id (str):
        merchant (str):
        market (str):
        product_name (str):
        price (float):
        old_price (float):
        currency (str):
        product_url (str):
        image_url (str):
    """

    id: str
    merchant: str
    market: str
    product_name: str
    price: float
    old_price: float
    currency: str
    product_url: str
    image_url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        merchant = self.merchant

        market = self.market

        product_name = self.product_name

        price = self.price

        old_price = self.old_price

        currency = self.currency

        product_url = self.product_url

        image_url = self.image_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "merchant": merchant,
                "market": market,
                "productName": product_name,
                "price": price,
                "oldPrice": old_price,
                "currency": currency,
                "productUrl": product_url,
                "imageUrl": image_url,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        merchant = d.pop("merchant")

        market = d.pop("market")

        product_name = d.pop("productName")

        price = d.pop("price")

        old_price = d.pop("oldPrice")

        currency = d.pop("currency")

        product_url = d.pop("productUrl")

        image_url = d.pop("imageUrl")

        barcode_affiliate_product_dto = cls(
            id=id,
            merchant=merchant,
            market=market,
            product_name=product_name,
            price=price,
            old_price=old_price,
            currency=currency,
            product_url=product_url,
            image_url=image_url,
        )

        barcode_affiliate_product_dto.additional_properties = d
        return barcode_affiliate_product_dto

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
