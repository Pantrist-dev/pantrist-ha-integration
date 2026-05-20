from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.merged_pantry_dto_list_pantry_ids import MergedPantryDtoListPantryIds
    from ..models.merged_pantry_dto_name_type_1 import MergedPantryDtoNameType1


T = TypeVar("T", bound="MergedPantryDto")


@_attrs_define
class MergedPantryDto:
    """
    Attributes:
        name (MergedPantryDtoNameType1 | str): Either a plain string or a translation key object
        list_pantry_ids (MergedPantryDtoListPantryIds): Map of listId → pantry uuid
        icon (None | str | Unset):
        location_type (None | str | Unset):
    """

    name: MergedPantryDtoNameType1 | str
    list_pantry_ids: MergedPantryDtoListPantryIds
    icon: None | str | Unset = UNSET
    location_type: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.merged_pantry_dto_name_type_1 import MergedPantryDtoNameType1

        name: dict[str, Any] | str
        if isinstance(self.name, MergedPantryDtoNameType1):
            name = self.name.to_dict()
        else:
            name = self.name

        list_pantry_ids = self.list_pantry_ids.to_dict()

        icon: None | str | Unset
        if isinstance(self.icon, Unset):
            icon = UNSET
        else:
            icon = self.icon

        location_type: None | str | Unset
        if isinstance(self.location_type, Unset):
            location_type = UNSET
        else:
            location_type = self.location_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "listPantryIds": list_pantry_ids,
            }
        )
        if icon is not UNSET:
            field_dict["icon"] = icon
        if location_type is not UNSET:
            field_dict["locationType"] = location_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.merged_pantry_dto_list_pantry_ids import MergedPantryDtoListPantryIds
        from ..models.merged_pantry_dto_name_type_1 import MergedPantryDtoNameType1

        d = dict(src_dict)

        def _parse_name(data: object) -> MergedPantryDtoNameType1 | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                name_type_1 = MergedPantryDtoNameType1.from_dict(data)

                return name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(MergedPantryDtoNameType1 | str, data)

        name = _parse_name(d.pop("name"))

        list_pantry_ids = MergedPantryDtoListPantryIds.from_dict(d.pop("listPantryIds"))

        def _parse_icon(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        icon = _parse_icon(d.pop("icon", UNSET))

        def _parse_location_type(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        location_type = _parse_location_type(d.pop("locationType", UNSET))

        merged_pantry_dto = cls(
            name=name,
            list_pantry_ids=list_pantry_ids,
            icon=icon,
            location_type=location_type,
        )

        merged_pantry_dto.additional_properties = d
        return merged_pantry_dto

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
