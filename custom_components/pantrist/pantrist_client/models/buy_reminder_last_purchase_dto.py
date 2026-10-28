from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BuyReminderLastPurchaseDto")


@_attrs_define
class BuyReminderLastPurchaseDto:
    """
    Attributes:
        name (str):
        content_volume (float):
        amount (float):
        brand (None | str | Unset):
        barcode (list[str] | None | Unset): Multi-barcode array (same shape as list_item.barcode).
        category_uuid (None | str | Unset):
        unit_id (None | str | Unset):
        supermarket_id (list[str] | None | Unset): Supermarket IDs the item was bought at (array column).
        price (float | None | Unset):
        price_type (None | str | Unset):
    """

    name: str
    content_volume: float
    amount: float
    brand: None | str | Unset = UNSET
    barcode: list[str] | None | Unset = UNSET
    category_uuid: None | str | Unset = UNSET
    unit_id: None | str | Unset = UNSET
    supermarket_id: list[str] | None | Unset = UNSET
    price: float | None | Unset = UNSET
    price_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        content_volume = self.content_volume

        amount = self.amount

        brand: None | str | Unset
        if isinstance(self.brand, Unset):
            brand = UNSET
        else:
            brand = self.brand

        barcode: list[str] | None | Unset
        if isinstance(self.barcode, Unset):
            barcode = UNSET
        elif isinstance(self.barcode, list):
            barcode = self.barcode

        else:
            barcode = self.barcode

        category_uuid: None | str | Unset
        if isinstance(self.category_uuid, Unset):
            category_uuid = UNSET
        else:
            category_uuid = self.category_uuid

        unit_id: None | str | Unset
        if isinstance(self.unit_id, Unset):
            unit_id = UNSET
        else:
            unit_id = self.unit_id

        supermarket_id: list[str] | None | Unset
        if isinstance(self.supermarket_id, Unset):
            supermarket_id = UNSET
        elif isinstance(self.supermarket_id, list):
            supermarket_id = self.supermarket_id

        else:
            supermarket_id = self.supermarket_id

        price: float | None | Unset
        if isinstance(self.price, Unset):
            price = UNSET
        else:
            price = self.price

        price_type: None | str | Unset
        if isinstance(self.price_type, Unset):
            price_type = UNSET
        else:
            price_type = self.price_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "contentVolume": content_volume,
                "amount": amount,
            }
        )
        if brand is not UNSET:
            field_dict["brand"] = brand
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if category_uuid is not UNSET:
            field_dict["categoryUuid"] = category_uuid
        if unit_id is not UNSET:
            field_dict["unitId"] = unit_id
        if supermarket_id is not UNSET:
            field_dict["supermarketId"] = supermarket_id
        if price is not UNSET:
            field_dict["price"] = price
        if price_type is not UNSET:
            field_dict["priceType"] = price_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        content_volume = d.pop("contentVolume")

        amount = d.pop("amount")

        def _parse_brand(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        brand = _parse_brand(d.pop("brand", UNSET))

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

        def _parse_category_uuid(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        category_uuid = _parse_category_uuid(d.pop("categoryUuid", UNSET))

        def _parse_unit_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        unit_id = _parse_unit_id(d.pop("unitId", UNSET))

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

        def _parse_price(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        price = _parse_price(d.pop("price", UNSET))

        def _parse_price_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        price_type = _parse_price_type(d.pop("priceType", UNSET))

        buy_reminder_last_purchase_dto = cls(
            name=name,
            content_volume=content_volume,
            amount=amount,
            brand=brand,
            barcode=barcode,
            category_uuid=category_uuid,
            unit_id=unit_id,
            supermarket_id=supermarket_id,
            price=price,
            price_type=price_type,
        )

        buy_reminder_last_purchase_dto.additional_properties = d
        return buy_reminder_last_purchase_dto

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
