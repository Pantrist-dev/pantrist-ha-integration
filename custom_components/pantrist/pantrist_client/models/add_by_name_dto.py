from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AddByNameDto")


@_attrs_define
class AddByNameDto:
    """
    Attributes:
        name (str):
        supermarket_ids (list[str] | Unset): Markets to buy the item at: `uid`s from GET /list/{listId}/supermarkets.
            Unknown ids are rejected with 400.
    """

    name: str
    supermarket_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        supermarket_ids: list[str] | Unset = UNSET
        if not isinstance(self.supermarket_ids, Unset):
            supermarket_ids = self.supermarket_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if supermarket_ids is not UNSET:
            field_dict["supermarketIds"] = supermarket_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        supermarket_ids = cast(list[str], d.pop("supermarketIds", UNSET))

        add_by_name_dto = cls(
            name=name,
            supermarket_ids=supermarket_ids,
        )

        add_by_name_dto.additional_properties = d
        return add_by_name_dto

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
