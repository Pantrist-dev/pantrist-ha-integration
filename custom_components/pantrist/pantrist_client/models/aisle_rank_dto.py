from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AisleRankDto")


@_attrs_define
class AisleRankDto:
    """
    Attributes:
        key (str): Category uuid, or a product key: `ing:<ingredientId>` when the purchase carried an ingredient, else
            the purchase product key (`bc:<first barcode>` or `nb:<lowercased trimmed name>|<lowercased trimmed brand>`).
        rank (float): Median relative position of the first check-off within a trip, 0 = first, 1 = last. Categories and
            products share the scale.
        name (str | Unset): Products only: the name it was last bought under in that market, for showing which articles
            the order covers.
        category (str | Unset): Products only: the category uuid it was last bought in there.
    """

    key: str
    rank: float
    name: str | Unset = UNSET
    category: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        key = self.key

        rank = self.rank

        name = self.name

        category = self.category

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "rank": rank,
            }
        )
        if name is not UNSET:
            field_dict["name"] = name
        if category is not UNSET:
            field_dict["category"] = category

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        key = d.pop("key")

        rank = d.pop("rank")

        name = d.pop("name", UNSET)

        category = d.pop("category", UNSET)

        aisle_rank_dto = cls(
            key=key,
            rank=rank,
            name=name,
            category=category,
        )

        aisle_rank_dto.additional_properties = d
        return aisle_rank_dto

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
