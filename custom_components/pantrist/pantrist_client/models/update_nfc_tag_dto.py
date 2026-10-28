from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UpdateNfcTagDto")


@_attrs_define
class UpdateNfcTagDto:
    """
    Attributes:
        item_id (str | Unset):
        amount_change (float | Unset):
        label (str | Unset):
    """

    item_id: str | Unset = UNSET
    amount_change: float | Unset = UNSET
    label: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        item_id = self.item_id

        amount_change = self.amount_change

        label = self.label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if item_id is not UNSET:
            field_dict["itemId"] = item_id
        if amount_change is not UNSET:
            field_dict["amountChange"] = amount_change
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        item_id = d.pop("itemId", UNSET)

        amount_change = d.pop("amountChange", UNSET)

        label = d.pop("label", UNSET)

        update_nfc_tag_dto = cls(
            item_id=item_id,
            amount_change=amount_change,
            label=label,
        )

        update_nfc_tag_dto.additional_properties = d
        return update_nfc_tag_dto

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
