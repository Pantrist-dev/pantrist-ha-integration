from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.volume_unit import VolumeUnit
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_product_group import ArticleProductGroup


T = TypeVar("T", bound="ItemDto")


@_attrs_define
class ItemDto:
    """
    Attributes:
        id (str): ID of the item
        name (str): Name of the item
        amount (float): Amount of the item
        content_volume (float): Content of a single item
        unit_id (VolumeUnit): Unit of the content. Besides the enum it's possible that custom IDs are used here
        barcode (list[str]): Barcode(s) of the product
        product_groups (list[ArticleProductGroup]): Product groups contain all relevant information about everything
            related to storage.
        brand (str | Unset): Brand of the item
    """

    id: str
    name: str
    amount: float
    content_volume: float
    unit_id: VolumeUnit
    barcode: list[str]
    product_groups: list[ArticleProductGroup]
    brand: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        amount = self.amount

        content_volume = self.content_volume

        unit_id = self.unit_id.value

        barcode = self.barcode

        product_groups = []
        for product_groups_item_data in self.product_groups:
            product_groups_item = product_groups_item_data.to_dict()
            product_groups.append(product_groups_item)

        brand = self.brand

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "amount": amount,
                "contentVolume": content_volume,
                "unitId": unit_id,
                "barcode": barcode,
                "productGroups": product_groups,
            }
        )
        if brand is not UNSET:
            field_dict["brand"] = brand

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_product_group import ArticleProductGroup

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        amount = d.pop("amount")

        content_volume = d.pop("contentVolume")

        unit_id = VolumeUnit(d.pop("unitId"))

        barcode = cast(list[str], d.pop("barcode"))

        product_groups = []
        _product_groups = d.pop("productGroups")
        for product_groups_item_data in _product_groups:
            product_groups_item = ArticleProductGroup.from_dict(product_groups_item_data)

            product_groups.append(product_groups_item)

        brand = d.pop("brand", UNSET)

        item_dto = cls(
            id=id,
            name=name,
            amount=amount,
            content_volume=content_volume,
            unit_id=unit_id,
            barcode=barcode,
            product_groups=product_groups,
            brand=brand,
        )

        item_dto.additional_properties = d
        return item_dto

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
