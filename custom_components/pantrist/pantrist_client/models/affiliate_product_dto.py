from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AffiliateProductDto")


@_attrs_define
class AffiliateProductDto:
    """
    Attributes:
        market (str):
        product_name (str):
        id (str | Unset):
        barcode (str | Unset):
        merchant (str | Unset):
        merchant_image (str | Unset):
        price (float | Unset):
        old_price (float | Unset):
        currency (str | Unset):
        product_url (str | Unset):
        image_url (str | Unset):
    """

    market: str
    product_name: str
    id: str | Unset = UNSET
    barcode: str | Unset = UNSET
    merchant: str | Unset = UNSET
    merchant_image: str | Unset = UNSET
    price: float | Unset = UNSET
    old_price: float | Unset = UNSET
    currency: str | Unset = UNSET
    product_url: str | Unset = UNSET
    image_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        market = self.market

        product_name = self.product_name

        id = self.id

        barcode = self.barcode

        merchant = self.merchant

        merchant_image = self.merchant_image

        price = self.price

        old_price = self.old_price

        currency = self.currency

        product_url = self.product_url

        image_url = self.image_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "market": market,
                "productName": product_name,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if merchant is not UNSET:
            field_dict["merchant"] = merchant
        if merchant_image is not UNSET:
            field_dict["merchantImage"] = merchant_image
        if price is not UNSET:
            field_dict["price"] = price
        if old_price is not UNSET:
            field_dict["oldPrice"] = old_price
        if currency is not UNSET:
            field_dict["currency"] = currency
        if product_url is not UNSET:
            field_dict["productUrl"] = product_url
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        market = d.pop("market")

        product_name = d.pop("productName")

        id = d.pop("id", UNSET)

        barcode = d.pop("barcode", UNSET)

        merchant = d.pop("merchant", UNSET)

        merchant_image = d.pop("merchantImage", UNSET)

        price = d.pop("price", UNSET)

        old_price = d.pop("oldPrice", UNSET)

        currency = d.pop("currency", UNSET)

        product_url = d.pop("productUrl", UNSET)

        image_url = d.pop("imageUrl", UNSET)

        affiliate_product_dto = cls(
            market=market,
            product_name=product_name,
            id=id,
            barcode=barcode,
            merchant=merchant,
            merchant_image=merchant_image,
            price=price,
            old_price=old_price,
            currency=currency,
            product_url=product_url,
            image_url=image_url,
        )

        affiliate_product_dto.additional_properties = d
        return affiliate_product_dto

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
