from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.merged_unit_dto_list_unit_ids import MergedUnitDtoListUnitIds


T = TypeVar("T", bound="MergedUnitDto")


@_attrs_define
class MergedUnitDto:
    """
    Attributes:
        name (str):
        list_unit_ids (MergedUnitDtoListUnitIds): Map of listId → unit uid
        plural (None | str | Unset):
        singular (None | str | Unset):
        show_at_item (bool | None | Unset):
        differentiation (bool | None | Unset):
    """

    name: str
    list_unit_ids: MergedUnitDtoListUnitIds
    plural: None | str | Unset = UNSET
    singular: None | str | Unset = UNSET
    show_at_item: bool | None | Unset = UNSET
    differentiation: bool | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        list_unit_ids = self.list_unit_ids.to_dict()

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "listUnitIds": list_unit_ids,
            }
        )
        if plural is not UNSET:
            field_dict["plural"] = plural
        if singular is not UNSET:
            field_dict["singular"] = singular
        if show_at_item is not UNSET:
            field_dict["showAtItem"] = show_at_item
        if differentiation is not UNSET:
            field_dict["differentiation"] = differentiation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.merged_unit_dto_list_unit_ids import MergedUnitDtoListUnitIds

        d = dict(src_dict)
        name = d.pop("name")

        list_unit_ids = MergedUnitDtoListUnitIds.from_dict(d.pop("listUnitIds"))

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

        merged_unit_dto = cls(
            name=name,
            list_unit_ids=list_unit_ids,
            plural=plural,
            singular=singular,
            show_at_item=show_at_item,
            differentiation=differentiation,
        )

        merged_unit_dto.additional_properties = d
        return merged_unit_dto

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
