from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.analysis_emergency_supply_settings_dto import AnalysisEmergencySupplySettingsDto


T = TypeVar("T", bound="AnalysisPantrySettingsDto")


@_attrs_define
class AnalysisPantrySettingsDto:
    """
    Attributes:
        people_count (float):
        pantry_filter (list[str] | Unset):
        food_categories (list[str] | Unset):
        beverages_categories (list[str] | Unset):
        nutriments_categories (list[str] | Unset):
        emergency_supply (AnalysisEmergencySupplySettingsDto | Unset):
    """

    people_count: float
    pantry_filter: list[str] | Unset = UNSET
    food_categories: list[str] | Unset = UNSET
    beverages_categories: list[str] | Unset = UNSET
    nutriments_categories: list[str] | Unset = UNSET
    emergency_supply: AnalysisEmergencySupplySettingsDto | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        people_count = self.people_count

        pantry_filter: list[str] | Unset = UNSET
        if not isinstance(self.pantry_filter, Unset):
            pantry_filter = self.pantry_filter

        food_categories: list[str] | Unset = UNSET
        if not isinstance(self.food_categories, Unset):
            food_categories = self.food_categories

        beverages_categories: list[str] | Unset = UNSET
        if not isinstance(self.beverages_categories, Unset):
            beverages_categories = self.beverages_categories

        nutriments_categories: list[str] | Unset = UNSET
        if not isinstance(self.nutriments_categories, Unset):
            nutriments_categories = self.nutriments_categories

        emergency_supply: dict[str, Any] | Unset = UNSET
        if not isinstance(self.emergency_supply, Unset):
            emergency_supply = self.emergency_supply.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "peopleCount": people_count,
            }
        )
        if pantry_filter is not UNSET:
            field_dict["pantryFilter"] = pantry_filter
        if food_categories is not UNSET:
            field_dict["foodCategories"] = food_categories
        if beverages_categories is not UNSET:
            field_dict["beveragesCategories"] = beverages_categories
        if nutriments_categories is not UNSET:
            field_dict["nutrimentsCategories"] = nutriments_categories
        if emergency_supply is not UNSET:
            field_dict["emergencySupply"] = emergency_supply

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.analysis_emergency_supply_settings_dto import AnalysisEmergencySupplySettingsDto

        d = dict(src_dict)
        people_count = d.pop("peopleCount")

        pantry_filter = cast(list[str], d.pop("pantryFilter", UNSET))

        food_categories = cast(list[str], d.pop("foodCategories", UNSET))

        beverages_categories = cast(list[str], d.pop("beveragesCategories", UNSET))

        nutriments_categories = cast(list[str], d.pop("nutrimentsCategories", UNSET))

        _emergency_supply = d.pop("emergencySupply", UNSET)
        emergency_supply: AnalysisEmergencySupplySettingsDto | Unset
        if isinstance(_emergency_supply, Unset):
            emergency_supply = UNSET
        else:
            emergency_supply = AnalysisEmergencySupplySettingsDto.from_dict(_emergency_supply)

        analysis_pantry_settings_dto = cls(
            people_count=people_count,
            pantry_filter=pantry_filter,
            food_categories=food_categories,
            beverages_categories=beverages_categories,
            nutriments_categories=nutriments_categories,
            emergency_supply=emergency_supply,
        )

        analysis_pantry_settings_dto.additional_properties = d
        return analysis_pantry_settings_dto

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
