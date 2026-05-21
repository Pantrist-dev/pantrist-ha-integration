from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CatalogMappingEntryDto")


@_attrs_define
class CatalogMappingEntryDto:
    """
    Attributes:
        receipt_name (str): Receipt name as recognised by OCR
        catalog_item_uuid (str): UUID of the matching article catalog item
    """

    receipt_name: str
    catalog_item_uuid: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        receipt_name = self.receipt_name

        catalog_item_uuid = self.catalog_item_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "receiptName": receipt_name,
                "catalogItemUuid": catalog_item_uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        receipt_name = d.pop("receiptName")

        catalog_item_uuid = d.pop("catalogItemUuid")

        catalog_mapping_entry_dto = cls(
            receipt_name=receipt_name,
            catalog_item_uuid=catalog_item_uuid,
        )

        catalog_mapping_entry_dto.additional_properties = d
        return catalog_mapping_entry_dto

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
