from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UnitDto")


@_attrs_define
class UnitDto:
    """
    Attributes:
        uid (str):
        name (str):
        show_at_item (bool):
        differentiation (bool):
        plural (str | Unset):
        singular (str | Unset):
    """

    uid: str
    name: str
    show_at_item: bool
    differentiation: bool
    plural: str | Unset = UNSET
    singular: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uid = self.uid

        name = self.name

        show_at_item = self.show_at_item

        differentiation = self.differentiation

        plural = self.plural

        singular = self.singular

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uid": uid,
                "name": name,
                "showAtItem": show_at_item,
                "differentiation": differentiation,
            }
        )
        if plural is not UNSET:
            field_dict["plural"] = plural
        if singular is not UNSET:
            field_dict["singular"] = singular

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uid = d.pop("uid")

        name = d.pop("name")

        show_at_item = d.pop("showAtItem")

        differentiation = d.pop("differentiation")

        plural = d.pop("plural", UNSET)

        singular = d.pop("singular", UNSET)

        unit_dto = cls(
            uid=uid,
            name=name,
            show_at_item=show_at_item,
            differentiation=differentiation,
            plural=plural,
            singular=singular,
        )

        unit_dto.additional_properties = d
        return unit_dto

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
