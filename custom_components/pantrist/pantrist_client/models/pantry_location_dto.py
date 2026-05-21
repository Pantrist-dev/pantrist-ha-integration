from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.location_type import LocationType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.pantry_location_dto_name_type_1 import PantryLocationDtoNameType1


T = TypeVar("T", bound="PantryLocationDto")


@_attrs_define
class PantryLocationDto:
    """
    Attributes:
        uuid (str):
        name (PantryLocationDtoNameType1 | str): Either a plain string or a translation key object
        is_favourite (bool):
        location_type (LocationType | None | Unset):
        icon (None | str | Unset):
        parent_location_id (None | str | Unset):
        list_id (str | Unset): Origin list of this pantry when returned by the cross-list "merged" endpoint in all-
            blocks mode. Not set on per-list responses.
    """

    uuid: str
    name: PantryLocationDtoNameType1 | str
    is_favourite: bool
    location_type: LocationType | None | Unset = UNSET
    icon: None | str | Unset = UNSET
    parent_location_id: None | str | Unset = UNSET
    list_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.pantry_location_dto_name_type_1 import PantryLocationDtoNameType1

        uuid = self.uuid

        name: dict[str, Any] | str
        if isinstance(self.name, PantryLocationDtoNameType1):
            name = self.name.to_dict()
        else:
            name = self.name

        is_favourite = self.is_favourite

        location_type: None | str | Unset
        if isinstance(self.location_type, Unset):
            location_type = UNSET
        elif isinstance(self.location_type, LocationType):
            location_type = self.location_type.value
        else:
            location_type = self.location_type

        icon: None | str | Unset
        if isinstance(self.icon, Unset):
            icon = UNSET
        else:
            icon = self.icon

        parent_location_id: None | str | Unset
        if isinstance(self.parent_location_id, Unset):
            parent_location_id = UNSET
        else:
            parent_location_id = self.parent_location_id

        list_id = self.list_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "isFavourite": is_favourite,
            }
        )
        if location_type is not UNSET:
            field_dict["locationType"] = location_type
        if icon is not UNSET:
            field_dict["icon"] = icon
        if parent_location_id is not UNSET:
            field_dict["parentLocationId"] = parent_location_id
        if list_id is not UNSET:
            field_dict["listId"] = list_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pantry_location_dto_name_type_1 import PantryLocationDtoNameType1

        d = dict(src_dict)
        uuid = d.pop("uuid")

        def _parse_name(data: object) -> PantryLocationDtoNameType1 | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                name_type_1 = PantryLocationDtoNameType1.from_dict(data)

                return name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(PantryLocationDtoNameType1 | str, data)

        name = _parse_name(d.pop("name"))

        is_favourite = d.pop("isFavourite")

        def _parse_location_type(data: object) -> LocationType | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                location_type_type_1 = LocationType(data)

                return location_type_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(LocationType | None | Unset, data)

        location_type = _parse_location_type(d.pop("locationType", UNSET))

        def _parse_icon(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        icon = _parse_icon(d.pop("icon", UNSET))

        def _parse_parent_location_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        parent_location_id = _parse_parent_location_id(d.pop("parentLocationId", UNSET))

        list_id = d.pop("listId", UNSET)

        pantry_location_dto = cls(
            uuid=uuid,
            name=name,
            is_favourite=is_favourite,
            location_type=location_type,
            icon=icon,
            parent_location_id=parent_location_id,
            list_id=list_id,
        )

        pantry_location_dto.additional_properties = d
        return pantry_location_dto

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
