from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.volume_unit import VolumeUnit
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_product_group import ArticleProductGroup


T = TypeVar("T", bound="UpdateItemDto")


@_attrs_define
class UpdateItemDto:
    """
    Attributes:
        name (str | Unset): Name of the item
        brand (str | Unset): Brand of the item
        content_volume (float | Unset): Content of a single item
        unit_id (VolumeUnit | Unset): Unit of the content. Besides the enum it's possible that custom IDs are used here
        barcode (list[str] | Unset): Barcode(s) of the product
        product_groups (list[ArticleProductGroup] | Unset): Product groups contain all relevant information about
            everything related to storage.
    """

    name: str | Unset = UNSET
    brand: str | Unset = UNSET
    content_volume: float | Unset = UNSET
    unit_id: VolumeUnit | Unset = UNSET
    barcode: list[str] | Unset = UNSET
    product_groups: list[ArticleProductGroup] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        brand = self.brand

        content_volume = self.content_volume

        unit_id: str | Unset = UNSET
        if not isinstance(self.unit_id, Unset):
            unit_id = self.unit_id.value

        barcode: list[str] | Unset = UNSET
        if not isinstance(self.barcode, Unset):
            barcode = self.barcode

        product_groups: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.product_groups, Unset):
            product_groups = []
            for product_groups_item_data in self.product_groups:
                product_groups_item = product_groups_item_data.to_dict()
                product_groups.append(product_groups_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if brand is not UNSET:
            field_dict["brand"] = brand
        if content_volume is not UNSET:
            field_dict["contentVolume"] = content_volume
        if unit_id is not UNSET:
            field_dict["unitId"] = unit_id
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if product_groups is not UNSET:
            field_dict["productGroups"] = product_groups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_product_group import ArticleProductGroup

        d = dict(src_dict)
        name = d.pop("name", UNSET)

        brand = d.pop("brand", UNSET)

        content_volume = d.pop("contentVolume", UNSET)

        _unit_id = d.pop("unitId", UNSET)
        unit_id: VolumeUnit | Unset
        if isinstance(_unit_id, Unset):
            unit_id = UNSET
        else:
            unit_id = VolumeUnit(_unit_id)

        barcode = cast(list[str], d.pop("barcode", UNSET))

        _product_groups = d.pop("productGroups", UNSET)
        product_groups: list[ArticleProductGroup] | Unset = UNSET
        if _product_groups is not UNSET:
            product_groups = []
            for product_groups_item_data in _product_groups:
                product_groups_item = ArticleProductGroup.from_dict(product_groups_item_data)

                product_groups.append(product_groups_item)

        update_item_dto = cls(
            name=name,
            brand=brand,
            content_volume=content_volume,
            unit_id=unit_id,
            barcode=barcode,
            product_groups=product_groups,
        )

        update_item_dto.additional_properties = d
        return update_item_dto

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
