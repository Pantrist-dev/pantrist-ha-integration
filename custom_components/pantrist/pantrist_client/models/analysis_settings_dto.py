from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.analysis_pantry_settings_dto import AnalysisPantrySettingsDto
    from ..models.analysis_shopping_settings_dto import AnalysisShoppingSettingsDto


T = TypeVar("T", bound="AnalysisSettingsDto")


@_attrs_define
class AnalysisSettingsDto:
    """
    Attributes:
        pantry (AnalysisPantrySettingsDto):
        shopping (AnalysisShoppingSettingsDto):
        field_updated_at (float | Unset):
    """

    pantry: AnalysisPantrySettingsDto
    shopping: AnalysisShoppingSettingsDto
    field_updated_at: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pantry = self.pantry.to_dict()

        shopping = self.shopping.to_dict()

        field_updated_at = self.field_updated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pantry": pantry,
                "shopping": shopping,
            }
        )
        if field_updated_at is not UNSET:
            field_dict["_updatedAt"] = field_updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.analysis_pantry_settings_dto import AnalysisPantrySettingsDto
        from ..models.analysis_shopping_settings_dto import AnalysisShoppingSettingsDto

        d = dict(src_dict)
        pantry = AnalysisPantrySettingsDto.from_dict(d.pop("pantry"))

        shopping = AnalysisShoppingSettingsDto.from_dict(d.pop("shopping"))

        field_updated_at = d.pop("_updatedAt", UNSET)

        analysis_settings_dto = cls(
            pantry=pantry,
            shopping=shopping,
            field_updated_at=field_updated_at,
        )

        analysis_settings_dto.additional_properties = d
        return analysis_settings_dto

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
