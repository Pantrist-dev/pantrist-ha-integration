from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.dietary_preferences_dto import DietaryPreferencesDto
    from ..models.shopping_list_settings_dto import ShoppingListSettingsDto
    from ..models.smart_suggestions_settings_dto import SmartSuggestionsSettingsDto


T = TypeVar("T", bound="BlockSettingsDto")


@_attrs_define
class BlockSettingsDto:
    """
    Attributes:
        name (str):
        enable_pantry (bool):
        shopping_list (ShoppingListSettingsDto):
        custom_currency (str | Unset):
        smart_suggestions (SmartSuggestionsSettingsDto | Unset):
        dietary_preferences (DietaryPreferencesDto | Unset):
        allow_to_open_articles (bool | Unset): When true, auto-restock discounts partially consumed open packages from
            the available amount (mirrors the app pantry setting). Defaults to true when unset.
    """

    name: str
    enable_pantry: bool
    shopping_list: ShoppingListSettingsDto
    custom_currency: str | Unset = UNSET
    smart_suggestions: SmartSuggestionsSettingsDto | Unset = UNSET
    dietary_preferences: DietaryPreferencesDto | Unset = UNSET
    allow_to_open_articles: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        enable_pantry = self.enable_pantry

        shopping_list = self.shopping_list.to_dict()

        custom_currency = self.custom_currency

        smart_suggestions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.smart_suggestions, Unset):
            smart_suggestions = self.smart_suggestions.to_dict()

        dietary_preferences: dict[str, Any] | Unset = UNSET
        if not isinstance(self.dietary_preferences, Unset):
            dietary_preferences = self.dietary_preferences.to_dict()

        allow_to_open_articles = self.allow_to_open_articles

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
        if smart_suggestions is not UNSET:
            field_dict["smartSuggestions"] = smart_suggestions
        if dietary_preferences is not UNSET:
            field_dict["dietaryPreferences"] = dietary_preferences
        if allow_to_open_articles is not UNSET:
            field_dict["allowToOpenArticles"] = allow_to_open_articles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.dietary_preferences_dto import DietaryPreferencesDto  # noqa: PLC0415
        from ..models.shopping_list_settings_dto import ShoppingListSettingsDto  # noqa: PLC0415
        from ..models.smart_suggestions_settings_dto import SmartSuggestionsSettingsDto  # noqa: PLC0415

        d = dict(src_dict)
        name = d.pop("name")

        enable_pantry = d.pop("enablePantry")

        shopping_list = ShoppingListSettingsDto.from_dict(d.pop("shoppingList"))

        custom_currency = d.pop("customCurrency", UNSET)

        _smart_suggestions = d.pop("smartSuggestions", UNSET)
        smart_suggestions: SmartSuggestionsSettingsDto | Unset
        if isinstance(_smart_suggestions, Unset) or _smart_suggestions is None:
            smart_suggestions = UNSET
        else:
            smart_suggestions = SmartSuggestionsSettingsDto.from_dict(_smart_suggestions)

        _dietary_preferences = d.pop("dietaryPreferences", UNSET)
        dietary_preferences: DietaryPreferencesDto | Unset
        if isinstance(_dietary_preferences, Unset) or _dietary_preferences is None:
            dietary_preferences = UNSET
        else:
            dietary_preferences = DietaryPreferencesDto.from_dict(_dietary_preferences)

        allow_to_open_articles = d.pop("allowToOpenArticles", UNSET)

        block_settings_dto = cls(
            name=name,
            enable_pantry=enable_pantry,
            shopping_list=shopping_list,
            custom_currency=custom_currency,
            smart_suggestions=smart_suggestions,
            dietary_preferences=dietary_preferences,
            allow_to_open_articles=allow_to_open_articles,
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
