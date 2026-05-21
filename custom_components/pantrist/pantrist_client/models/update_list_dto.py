from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.block_settings_dto import BlockSettingsDto


T = TypeVar("T", bound="UpdateListDto")


@_attrs_define
class UpdateListDto:
    """
    Attributes:
        settings (BlockSettingsDto | Unset):
        name (str | Unset): Updated list name
    """

    settings: BlockSettingsDto | Unset = UNSET
    name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if settings is not UNSET:
            field_dict["settings"] = settings
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.block_settings_dto import BlockSettingsDto

        d = dict(src_dict)
        _settings = d.pop("settings", UNSET)
        settings: BlockSettingsDto | Unset
        if isinstance(_settings, Unset) or _settings is None:
            settings = UNSET
        else:
            settings = BlockSettingsDto.from_dict(_settings)

        name = d.pop("name", UNSET)

        update_list_dto = cls(
            settings=settings,
            name=name,
        )

        update_list_dto.additional_properties = d
        return update_list_dto

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
