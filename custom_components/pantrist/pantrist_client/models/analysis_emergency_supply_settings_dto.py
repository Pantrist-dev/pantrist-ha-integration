from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.analysis_emergency_supply_settings_dto_standard import AnalysisEmergencySupplySettingsDtoStandard

if TYPE_CHECKING:
    from ..models.analysis_emergency_supply_settings_dto_mappings import AnalysisEmergencySupplySettingsDtoMappings


T = TypeVar("T", bound="AnalysisEmergencySupplySettingsDto")


@_attrs_define
class AnalysisEmergencySupplySettingsDto:
    """
    Attributes:
        enabled (bool):
        standard (AnalysisEmergencySupplySettingsDtoStandard):
        mappings (AnalysisEmergencySupplySettingsDtoMappings):
    """

    enabled: bool
    standard: AnalysisEmergencySupplySettingsDtoStandard
    mappings: AnalysisEmergencySupplySettingsDtoMappings
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        standard = self.standard.value

        mappings = self.mappings.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "standard": standard,
                "mappings": mappings,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.analysis_emergency_supply_settings_dto_mappings import AnalysisEmergencySupplySettingsDtoMappings

        d = dict(src_dict)
        enabled = d.pop("enabled")

        standard = AnalysisEmergencySupplySettingsDtoStandard(d.pop("standard"))

        mappings = AnalysisEmergencySupplySettingsDtoMappings.from_dict(d.pop("mappings"))

        analysis_emergency_supply_settings_dto = cls(
            enabled=enabled,
            standard=standard,
            mappings=mappings,
        )

        analysis_emergency_supply_settings_dto.additional_properties = d
        return analysis_emergency_supply_settings_dto

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
