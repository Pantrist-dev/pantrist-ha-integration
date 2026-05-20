from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ListDto")


@_attrs_define
class ListDto:
    """
    Attributes:
        id (str): ID of the list
        name (str): Name of the list
        user_count (float): Count of users that have access to the list.
        current_list (bool): Whether the list is your current list.
    """

    id: str
    name: str
    user_count: float
    current_list: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        user_count = self.user_count

        current_list = self.current_list

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "userCount": user_count,
                "currentList": current_list,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        user_count = d.pop("userCount")

        current_list = d.pop("currentList")

        list_dto = cls(
            id=id,
            name=name,
            user_count=user_count,
            current_list=current_list,
        )

        list_dto.additional_properties = d
        return list_dto

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
