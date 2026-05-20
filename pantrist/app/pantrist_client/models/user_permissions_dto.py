from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserPermissionsDto")


@_attrs_define
class UserPermissionsDto:
    """
    Attributes:
        is_not_allowed_to_add_recipes (bool | Unset):
        is_not_allowed_to_report_recipes (bool | Unset):
        is_not_allowed_to_change_barcode_data (bool | Unset):
    """

    is_not_allowed_to_add_recipes: bool | Unset = UNSET
    is_not_allowed_to_report_recipes: bool | Unset = UNSET
    is_not_allowed_to_change_barcode_data: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_not_allowed_to_add_recipes = self.is_not_allowed_to_add_recipes

        is_not_allowed_to_report_recipes = self.is_not_allowed_to_report_recipes

        is_not_allowed_to_change_barcode_data = self.is_not_allowed_to_change_barcode_data

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_not_allowed_to_add_recipes is not UNSET:
            field_dict["isNotAllowedToAddRecipes"] = is_not_allowed_to_add_recipes
        if is_not_allowed_to_report_recipes is not UNSET:
            field_dict["isNotAllowedToReportRecipes"] = is_not_allowed_to_report_recipes
        if is_not_allowed_to_change_barcode_data is not UNSET:
            field_dict["isNotAllowedToChangeBarcodeData"] = is_not_allowed_to_change_barcode_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        is_not_allowed_to_add_recipes = d.pop("isNotAllowedToAddRecipes", UNSET)

        is_not_allowed_to_report_recipes = d.pop("isNotAllowedToReportRecipes", UNSET)

        is_not_allowed_to_change_barcode_data = d.pop("isNotAllowedToChangeBarcodeData", UNSET)

        user_permissions_dto = cls(
            is_not_allowed_to_add_recipes=is_not_allowed_to_add_recipes,
            is_not_allowed_to_report_recipes=is_not_allowed_to_report_recipes,
            is_not_allowed_to_change_barcode_data=is_not_allowed_to_change_barcode_data,
        )

        user_permissions_dto.additional_properties = d
        return user_permissions_dto

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
