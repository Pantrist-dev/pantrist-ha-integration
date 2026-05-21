from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PantrySettingsDto")


@_attrs_define
class PantrySettingsDto:
    """
    Attributes:
        pantry_uuid (str):
        count (float | Unset):
        best_before (str | Unset):
        calculated_best_before_date (bool | Unset):
        article_is_open (bool | Unset):
        article_is_open_since (float | str | Unset):
        remaining_amount (float | Unset):
    """

    pantry_uuid: str
    count: float | Unset = UNSET
    best_before: str | Unset = UNSET
    calculated_best_before_date: bool | Unset = UNSET
    article_is_open: bool | Unset = UNSET
    article_is_open_since: float | str | Unset = UNSET
    remaining_amount: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pantry_uuid = self.pantry_uuid

        count = self.count

        best_before = self.best_before

        calculated_best_before_date = self.calculated_best_before_date

        article_is_open = self.article_is_open

        article_is_open_since: float | str | Unset
        if isinstance(self.article_is_open_since, Unset):
            article_is_open_since = UNSET
        else:
            article_is_open_since = self.article_is_open_since

        remaining_amount = self.remaining_amount

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pantryUuid": pantry_uuid,
            }
        )
        if count is not UNSET:
            field_dict["count"] = count
        if best_before is not UNSET:
            field_dict["bestBefore"] = best_before
        if calculated_best_before_date is not UNSET:
            field_dict["calculatedBestBeforeDate"] = calculated_best_before_date
        if article_is_open is not UNSET:
            field_dict["articleIsOpen"] = article_is_open
        if article_is_open_since is not UNSET:
            field_dict["articleIsOpenSince"] = article_is_open_since
        if remaining_amount is not UNSET:
            field_dict["remainingAmount"] = remaining_amount

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        pantry_uuid = d.pop("pantryUuid")

        count = d.pop("count", UNSET)

        best_before = d.pop("bestBefore", UNSET)

        calculated_best_before_date = d.pop("calculatedBestBeforeDate", UNSET)

        article_is_open = d.pop("articleIsOpen", UNSET)

        def _parse_article_is_open_since(data: object) -> float | str | Unset:
            if isinstance(data, Unset):
                return data
            return cast(float | str | Unset, data)

        article_is_open_since = _parse_article_is_open_since(d.pop("articleIsOpenSince", UNSET))

        remaining_amount = d.pop("remainingAmount", UNSET)

        pantry_settings_dto = cls(
            pantry_uuid=pantry_uuid,
            count=count,
            best_before=best_before,
            calculated_best_before_date=calculated_best_before_date,
            article_is_open=article_is_open,
            article_is_open_since=article_is_open_since,
            remaining_amount=remaining_amount,
        )

        pantry_settings_dto.additional_properties = d
        return pantry_settings_dto

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
