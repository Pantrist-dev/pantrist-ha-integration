from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.price_trend_content_change_dto import PriceTrendContentChangeDto
    from ..models.purchased_item_dto import PurchasedItemDto


T = TypeVar("T", bound="PriceTrendDetailDto")


@_attrs_define
class PriceTrendDetailDto:
    """
    Attributes:
        product_key (str):
        name (str):
        purchases (list[PurchasedItemDto]):
        content_changes (list[PriceTrendContentChangeDto]):
        brand (str | Unset):
        barcode (str | Unset):
    """

    product_key: str
    name: str
    purchases: list[PurchasedItemDto]
    content_changes: list[PriceTrendContentChangeDto]
    brand: str | Unset = UNSET
    barcode: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        product_key = self.product_key

        name = self.name

        purchases = []
        for purchases_item_data in self.purchases:
            purchases_item = purchases_item_data.to_dict()
            purchases.append(purchases_item)

        content_changes = []
        for content_changes_item_data in self.content_changes:
            content_changes_item = content_changes_item_data.to_dict()
            content_changes.append(content_changes_item)

        brand = self.brand

        barcode = self.barcode

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "productKey": product_key,
                "name": name,
                "purchases": purchases,
                "contentChanges": content_changes,
            }
        )
        if brand is not UNSET:
            field_dict["brand"] = brand
        if barcode is not UNSET:
            field_dict["barcode"] = barcode

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.price_trend_content_change_dto import PriceTrendContentChangeDto  # noqa: PLC0415
        from ..models.purchased_item_dto import PurchasedItemDto  # noqa: PLC0415

        d = dict(src_dict)
        product_key = d.pop("productKey")

        name = d.pop("name")

        purchases = []
        _purchases = d.pop("purchases")
        for purchases_item_data in _purchases:
            purchases_item = PurchasedItemDto.from_dict(purchases_item_data)

            purchases.append(purchases_item)

        content_changes = []
        _content_changes = d.pop("contentChanges")
        for content_changes_item_data in _content_changes:
            content_changes_item = PriceTrendContentChangeDto.from_dict(content_changes_item_data)

            content_changes.append(content_changes_item)

        brand = d.pop("brand", UNSET)

        barcode = d.pop("barcode", UNSET)

        price_trend_detail_dto = cls(
            product_key=product_key,
            name=name,
            purchases=purchases,
            content_changes=content_changes,
            brand=brand,
            barcode=barcode,
        )

        price_trend_detail_dto.additional_properties = d
        return price_trend_detail_dto

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
