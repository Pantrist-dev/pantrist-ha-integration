from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SmartSuggestionsSettingsDto")


@_attrs_define
class SmartSuggestionsSettingsDto:
    """
    Attributes:
        auto_reduce_enabled (bool | Unset):
        buy_reminders_enabled (bool | Unset):
        default_auto_reduce (bool | Unset): When true, items without explicit auto-reduce config but with high-
            confidence consumption history are auto-included in the cold-start accrual modal.
    """

    auto_reduce_enabled: bool | Unset = UNSET
    buy_reminders_enabled: bool | Unset = UNSET
    default_auto_reduce: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        auto_reduce_enabled = self.auto_reduce_enabled

        buy_reminders_enabled = self.buy_reminders_enabled

        default_auto_reduce = self.default_auto_reduce

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if auto_reduce_enabled is not UNSET:
            field_dict["autoReduceEnabled"] = auto_reduce_enabled
        if buy_reminders_enabled is not UNSET:
            field_dict["buyRemindersEnabled"] = buy_reminders_enabled
        if default_auto_reduce is not UNSET:
            field_dict["defaultAutoReduce"] = default_auto_reduce

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        auto_reduce_enabled = d.pop("autoReduceEnabled", UNSET)

        buy_reminders_enabled = d.pop("buyRemindersEnabled", UNSET)

        default_auto_reduce = d.pop("defaultAutoReduce", UNSET)

        smart_suggestions_settings_dto = cls(
            auto_reduce_enabled=auto_reduce_enabled,
            buy_reminders_enabled=buy_reminders_enabled,
            default_auto_reduce=default_auto_reduce,
        )

        smart_suggestions_settings_dto.additional_properties = d
        return smart_suggestions_settings_dto

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
