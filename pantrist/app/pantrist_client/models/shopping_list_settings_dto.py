from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ShoppingListSettingsDto")


@_attrs_define
class ShoppingListSettingsDto:
    """
    Attributes:
        show_intermediate_list (bool):
        move_element_to_pantry_on_check (bool | Unset):
        ask_for_best_until_before_moving (bool | Unset):
        ask_for_data_when_moving_to_the_cart (bool | Unset):
    """

    show_intermediate_list: bool
    move_element_to_pantry_on_check: bool | Unset = UNSET
    ask_for_best_until_before_moving: bool | Unset = UNSET
    ask_for_data_when_moving_to_the_cart: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        show_intermediate_list = self.show_intermediate_list

        move_element_to_pantry_on_check = self.move_element_to_pantry_on_check

        ask_for_best_until_before_moving = self.ask_for_best_until_before_moving

        ask_for_data_when_moving_to_the_cart = self.ask_for_data_when_moving_to_the_cart

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "showIntermediateList": show_intermediate_list,
            }
        )
        if move_element_to_pantry_on_check is not UNSET:
            field_dict["moveElementToPantryOnCheck"] = move_element_to_pantry_on_check
        if ask_for_best_until_before_moving is not UNSET:
            field_dict["askForBestUntilBeforeMoving"] = ask_for_best_until_before_moving
        if ask_for_data_when_moving_to_the_cart is not UNSET:
            field_dict["askForDataWhenMovingToTheCart"] = ask_for_data_when_moving_to_the_cart

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        show_intermediate_list = d.pop("showIntermediateList")

        move_element_to_pantry_on_check = d.pop("moveElementToPantryOnCheck", UNSET)

        ask_for_best_until_before_moving = d.pop("askForBestUntilBeforeMoving", UNSET)

        ask_for_data_when_moving_to_the_cart = d.pop("askForDataWhenMovingToTheCart", UNSET)

        shopping_list_settings_dto = cls(
            show_intermediate_list=show_intermediate_list,
            move_element_to_pantry_on_check=move_element_to_pantry_on_check,
            ask_for_best_until_before_moving=ask_for_best_until_before_moving,
            ask_for_data_when_moving_to_the_cart=ask_for_data_when_moving_to_the_cart,
        )

        shopping_list_settings_dto.additional_properties = d
        return shopping_list_settings_dto

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
