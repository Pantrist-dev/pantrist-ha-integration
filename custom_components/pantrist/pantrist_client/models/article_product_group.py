from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArticleProductGroup")


@_attrs_define
class ArticleProductGroup:
    """
    Attributes:
        index (float): Index of the group inside the product group list
        count (float): Products inside the product group
        pantry_id (str): ID of the location
        article_is_open (bool): Indicates whether the product group contains an opened product
        best_before (str | Unset): Best before date in that group
        remaining_amount (float | Unset): Remaining amount in the opened product
    """

    index: float
    count: float
    pantry_id: str
    article_is_open: bool
    best_before: str | Unset = UNSET
    remaining_amount: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        index = self.index

        count = self.count

        pantry_id = self.pantry_id

        article_is_open = self.article_is_open

        best_before = self.best_before

        remaining_amount = self.remaining_amount

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "index": index,
                "count": count,
                "pantryId": pantry_id,
                "articleIsOpen": article_is_open,
            }
        )
        if best_before is not UNSET:
            field_dict["bestBefore"] = best_before
        if remaining_amount is not UNSET:
            field_dict["remainingAmount"] = remaining_amount

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        index = d.pop("index")

        count = d.pop("count")

        pantry_id = d.pop("pantryId")

        article_is_open = d.pop("articleIsOpen")

        best_before = d.pop("bestBefore", UNSET)

        remaining_amount = d.pop("remainingAmount", UNSET)

        article_product_group = cls(
            index=index,
            count=count,
            pantry_id=pantry_id,
            article_is_open=article_is_open,
            best_before=best_before,
            remaining_amount=remaining_amount,
        )

        article_product_group.additional_properties = d
        return article_product_group

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
