from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SupermarketDto")


@_attrs_define
class SupermarketDto:
    """
    Attributes:
        uid (str):
        name (str):
        icon_id (str):
        category_sort_order (list[str] | None | Unset):
        different_order (bool | None | Unset):
    """

    uid: str
    name: str
    icon_id: str
    category_sort_order: list[str] | None | Unset = UNSET
    different_order: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uid = self.uid

        name = self.name

        icon_id = self.icon_id

        category_sort_order: list[str] | None | Unset
        if isinstance(self.category_sort_order, Unset):
            category_sort_order = UNSET
        elif isinstance(self.category_sort_order, list):
            category_sort_order = self.category_sort_order

        else:
            category_sort_order = self.category_sort_order

        different_order: bool | None | Unset
        if isinstance(self.different_order, Unset):
            different_order = UNSET
        else:
            different_order = self.different_order

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uid": uid,
                "name": name,
                "iconId": icon_id,
            }
        )
        if category_sort_order is not UNSET:
            field_dict["categorySortOrder"] = category_sort_order
        if different_order is not UNSET:
            field_dict["differentOrder"] = different_order

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uid = d.pop("uid")

        name = d.pop("name")

        icon_id = d.pop("iconId")

        def _parse_category_sort_order(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                category_sort_order_type_0 = cast(list[str], data)

                return category_sort_order_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        category_sort_order = _parse_category_sort_order(d.pop("categorySortOrder", UNSET))

        def _parse_different_order(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        different_order = _parse_different_order(d.pop("differentOrder", UNSET))

        supermarket_dto = cls(
            uid=uid,
            name=name,
            icon_id=icon_id,
            category_sort_order=category_sort_order,
            different_order=different_order,
        )

        supermarket_dto.additional_properties = d
        return supermarket_dto

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
