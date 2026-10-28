from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="NfcTagDto")


@_attrs_define
class NfcTagDto:
    """
    Attributes:
        id (str):
        list_id (str):
        item_id (None | str): UUID of the linked pantry article, or null if that article was deleted.
        amount_change (float):
        label (None | str):
        last_written_at (float | None): Epoch milliseconds when the tag was last successfully written to a physical NFC
            tag, or null if never written.
        created_at (datetime.datetime):
    """

    id: str
    list_id: str
    item_id: None | str
    amount_change: float
    label: None | str
    last_written_at: float | None
    created_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        list_id = self.list_id

        item_id: None | str
        item_id = self.item_id

        amount_change = self.amount_change

        label: None | str
        label = self.label

        last_written_at: float | None
        last_written_at = self.last_written_at

        created_at = self.created_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "listId": list_id,
                "itemId": item_id,
                "amountChange": amount_change,
                "label": label,
                "lastWrittenAt": last_written_at,
                "createdAt": created_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        list_id = d.pop("listId")

        def _parse_item_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        item_id = _parse_item_id(d.pop("itemId"))

        amount_change = d.pop("amountChange")

        def _parse_label(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        label = _parse_label(d.pop("label"))

        def _parse_last_written_at(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        last_written_at = _parse_last_written_at(d.pop("lastWrittenAt"))

        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))

        nfc_tag_dto = cls(
            id=id,
            list_id=list_id,
            item_id=item_id,
            amount_change=amount_change,
            label=label,
            last_written_at=last_written_at,
            created_at=created_at,
        )

        nfc_tag_dto.additional_properties = d
        return nfc_tag_dto

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
