from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.purchased_item_dto_discount_type import PurchasedItemDtoDiscountType
from ..models.purchased_item_dto_price_type import PurchasedItemDtoPriceType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PurchasedItemDto")


@_attrs_define
class PurchasedItemDto:
    """
    Attributes:
        uuid (str):
        name (str):
        amount (float):
        category_uuid (str):
        content_volume (float):
        unit_id (str):
        purchase_date (str): ISO date string
        price_type (PurchasedItemDtoPriceType):
        discount_type (PurchasedItemDtoDiscountType):
        purchase_row_id (str | Unset): Row primary key in purchase table — used for DELETE
        brand (str | Unset):
        barcode (list[str] | str | Unset):
        supermarket_id (str | Unset):
        price (float | Unset):
        deposit (float | Unset):
        discount (float | Unset):
        coupon_name (str | Unset):
        coupon_expiration_date (str | Unset):
    """

    uuid: str
    name: str
    amount: float
    category_uuid: str
    content_volume: float
    unit_id: str
    purchase_date: str
    price_type: PurchasedItemDtoPriceType
    discount_type: PurchasedItemDtoDiscountType
    purchase_row_id: str | Unset = UNSET
    brand: str | Unset = UNSET
    barcode: list[str] | str | Unset = UNSET
    supermarket_id: str | Unset = UNSET
    price: float | Unset = UNSET
    deposit: float | Unset = UNSET
    discount: float | Unset = UNSET
    coupon_name: str | Unset = UNSET
    coupon_expiration_date: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        name = self.name

        amount = self.amount

        category_uuid = self.category_uuid

        content_volume = self.content_volume

        unit_id = self.unit_id

        purchase_date = self.purchase_date

        price_type = self.price_type.value

        discount_type = self.discount_type.value

        purchase_row_id = self.purchase_row_id

        brand = self.brand

        barcode: list[str] | str | Unset
        if isinstance(self.barcode, Unset):
            barcode = UNSET
        elif isinstance(self.barcode, list):
            barcode = self.barcode

        else:
            barcode = self.barcode

        supermarket_id = self.supermarket_id

        price = self.price

        deposit = self.deposit

        discount = self.discount

        coupon_name = self.coupon_name

        coupon_expiration_date = self.coupon_expiration_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "amount": amount,
                "categoryUuid": category_uuid,
                "contentVolume": content_volume,
                "unitId": unit_id,
                "purchaseDate": purchase_date,
                "priceType": price_type,
                "discountType": discount_type,
            }
        )
        if purchase_row_id is not UNSET:
            field_dict["purchaseRowId"] = purchase_row_id
        if brand is not UNSET:
            field_dict["brand"] = brand
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if supermarket_id is not UNSET:
            field_dict["supermarketId"] = supermarket_id
        if price is not UNSET:
            field_dict["price"] = price
        if deposit is not UNSET:
            field_dict["deposit"] = deposit
        if discount is not UNSET:
            field_dict["discount"] = discount
        if coupon_name is not UNSET:
            field_dict["couponName"] = coupon_name
        if coupon_expiration_date is not UNSET:
            field_dict["couponExpirationDate"] = coupon_expiration_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        name = d.pop("name")

        amount = d.pop("amount")

        category_uuid = d.pop("categoryUuid")

        content_volume = d.pop("contentVolume")

        unit_id = d.pop("unitId")

        purchase_date = d.pop("purchaseDate")

        price_type = PurchasedItemDtoPriceType(d.pop("priceType"))

        discount_type = PurchasedItemDtoDiscountType(d.pop("discountType"))

        purchase_row_id = d.pop("purchaseRowId", UNSET)

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

        supermarket_id = d.pop("supermarketId", UNSET)

        price = d.pop("price", UNSET)

        deposit = d.pop("deposit", UNSET)

        discount = d.pop("discount", UNSET)

        coupon_name = d.pop("couponName", UNSET)

        coupon_expiration_date = d.pop("couponExpirationDate", UNSET)

        purchased_item_dto = cls(
            uuid=uuid,
            name=name,
            amount=amount,
            category_uuid=category_uuid,
            content_volume=content_volume,
            unit_id=unit_id,
            purchase_date=purchase_date,
            price_type=price_type,
            discount_type=discount_type,
            purchase_row_id=purchase_row_id,
            brand=brand,
            barcode=barcode,
            supermarket_id=supermarket_id,
            price=price,
            deposit=deposit,
            discount=discount,
            coupon_name=coupon_name,
            coupon_expiration_date=coupon_expiration_date,
        )

        purchased_item_dto.additional_properties = d
        return purchased_item_dto

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
