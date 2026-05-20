from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

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
        show_at_item (bool | None | Unset):
        differentiation (bool | None | Unset):
        plural (None | str | Unset):
        singular (None | str | Unset):
        list_id (str | Unset): Origin list of this unit when returned by the cross-list "merged" endpoint in all-blocks
            mode. Not set on per-list responses.
    """

    uid: str
    name: str
    show_at_item: bool | None | Unset = UNSET
    differentiation: bool | None | Unset = UNSET
    plural: None | str | Unset = UNSET
    singular: None | str | Unset = UNSET
    list_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uid = self.uid

        name = self.name

        show_at_item: bool | None | Unset
        if isinstance(self.show_at_item, Unset):
            show_at_item = UNSET
        else:
            show_at_item = self.show_at_item

        differentiation: bool | None | Unset
        if isinstance(self.differentiation, Unset):
            differentiation = UNSET
        else:
            differentiation = self.differentiation

        plural: None | str | Unset
        if isinstance(self.plural, Unset):
            plural = UNSET
        else:
            plural = self.plural

        singular: None | str | Unset
        if isinstance(self.singular, Unset):
            singular = UNSET
        else:
            singular = self.singular

        list_id = self.list_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uid": uid,
                "name": name,
            }
        )
        if show_at_item is not UNSET:
            field_dict["showAtItem"] = show_at_item
        if differentiation is not UNSET:
            field_dict["differentiation"] = differentiation
        if plural is not UNSET:
            field_dict["plural"] = plural
        if singular is not UNSET:
            field_dict["singular"] = singular
        if list_id is not UNSET:
            field_dict["listId"] = list_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uid = d.pop("uid")

        name = d.pop("name")

        def _parse_show_at_item(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        show_at_item = _parse_show_at_item(d.pop("showAtItem", UNSET))

        def _parse_differentiation(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        differentiation = _parse_differentiation(d.pop("differentiation", UNSET))

        def _parse_plural(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        plural = _parse_plural(d.pop("plural", UNSET))

        def _parse_singular(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        singular = _parse_singular(d.pop("singular", UNSET))

        list_id = d.pop("listId", UNSET)

        unit_dto = cls(
            uid=uid,
            name=name,
            show_at_item=show_at_item,
            differentiation=differentiation,
            plural=plural,
            singular=singular,
            list_id=list_id,
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
