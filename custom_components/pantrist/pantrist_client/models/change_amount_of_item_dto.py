from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

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
    """

    amount_change: float
    product_group_index: float | Unset = UNSET
    pantry_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount_change = self.amount_change

        product_group_index = self.product_group_index

        pantry_id = self.pantry_id

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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount_change = d.pop("amountChange")

        product_group_index = d.pop("productGroupIndex", UNSET)

        pantry_id = d.pop("pantryId", UNSET)

        change_amount_of_item_dto = cls(
            amount_change=amount_change,
            product_group_index=product_group_index,
            pantry_id=pantry_id,
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
