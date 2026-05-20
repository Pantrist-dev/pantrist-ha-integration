from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.shopping_list_settings_dto import ShoppingListSettingsDto


T = TypeVar("T", bound="BlockSettingsDto")


@_attrs_define
class BlockSettingsDto:
    """
    Attributes:
        name (str):
        enable_pantry (bool):
        shopping_list (ShoppingListSettingsDto):
        custom_currency (str | Unset):
    """

    name: str
    enable_pantry: bool
    shopping_list: ShoppingListSettingsDto
    custom_currency: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        enable_pantry = self.enable_pantry

        shopping_list = self.shopping_list.to_dict()

        custom_currency = self.custom_currency

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "enablePantry": enable_pantry,
                "shoppingList": shopping_list,
            }
        )
        if custom_currency is not UNSET:
            field_dict["customCurrency"] = custom_currency

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.shopping_list_settings_dto import ShoppingListSettingsDto

        d = dict(src_dict)
        name = d.pop("name")

        enable_pantry = d.pop("enablePantry")

        shopping_list = ShoppingListSettingsDto.from_dict(d.pop("shoppingList"))

        custom_currency = d.pop("customCurrency", UNSET)

        block_settings_dto = cls(
            name=name,
            enable_pantry=enable_pantry,
            shopping_list=shopping_list,
            custom_currency=custom_currency,
        )

        block_settings_dto.additional_properties = d
        return block_settings_dto

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
