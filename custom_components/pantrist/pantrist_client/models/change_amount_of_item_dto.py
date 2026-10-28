from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.change_amount_of_item_dto_source import ChangeAmountOfItemDtoSource
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangeAmountOfItemDto")


@_attrs_define
class ChangeAmountOfItemDto:
    """
    Attributes:
        amount_change (float): New amount of the item
        product_group_index (float | Unset): Index of the product group to change the amount of
        pantry_id (str | Unset): Pantry id of the product group you want to change the amount of. If no group is found,
            a new one will be created
        auto_restock (bool | Unset): When true, and the resulting pantry amount lands at or below the item's configured
            `minimumAmount` (with `manageMinimumAmount` enabled; counted in content when `minimumAmountMode` is `content`),
            the server also adds the item to the shopping list by name. Designed for automation clients (Home Assistant NFC
            scans, voice assistants, etc.) that want a single round-trip 'consume + reorder' contract. Defaults to false so
            app-driven decrements keep their current behaviour. Default: False.
        source (ChangeAmountOfItemDtoSource | Unset): Optional tag describing where the change originated. Written to
            `amount_change_log.source`. Defaults to `manual`.
    """

    amount_change: float
    product_group_index: float | Unset = UNSET
    pantry_id: str | Unset = UNSET
    auto_restock: bool | Unset = False
    source: ChangeAmountOfItemDtoSource | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount_change = self.amount_change

        product_group_index = self.product_group_index

        pantry_id = self.pantry_id

        auto_restock = self.auto_restock

        source: str | Unset = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amountChange": amount_change,
            }
        )
        if product_group_index is not UNSET:
            field_dict["productGroupIndex"] = product_group_index
        if pantry_id is not UNSET:
            field_dict["pantryId"] = pantry_id
        if auto_restock is not UNSET:
            field_dict["autoRestock"] = auto_restock
        if source is not UNSET:
            field_dict["source"] = source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount_change = d.pop("amountChange")

        product_group_index = d.pop("productGroupIndex", UNSET)

        pantry_id = d.pop("pantryId", UNSET)

        auto_restock = d.pop("autoRestock", UNSET)

        _source = d.pop("source", UNSET)
        source: ChangeAmountOfItemDtoSource | Unset
        if isinstance(_source, Unset) or _source is None or _source == "":
            source = UNSET
        else:
            source = ChangeAmountOfItemDtoSource(_source)

        change_amount_of_item_dto = cls(
            amount_change=amount_change,
            product_group_index=product_group_index,
            pantry_id=pantry_id,
            auto_restock=auto_restock,
            source=source,
        )

        change_amount_of_item_dto.additional_properties = d
        return change_amount_of_item_dto

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
