from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_nutriments_dto import ArticleNutrimentsDto


T = TypeVar("T", bound="ParseNutrimentsResultDto")


@_attrs_define
class ParseNutrimentsResultDto:
    """
    Attributes:
        nutriments (ArticleNutrimentsDto | Unset):
        allergens (list[str] | Unset): EU 14 allergens found in the ingredients.
    """

    nutriments: ArticleNutrimentsDto | Unset = UNSET
    allergens: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        nutriments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.nutriments, Unset):
            nutriments = self.nutriments.to_dict()

        allergens: list[str] | Unset = UNSET
        if not isinstance(self.allergens, Unset):
            allergens = self.allergens

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if nutriments is not UNSET:
            field_dict["nutriments"] = nutriments
        if allergens is not UNSET:
            field_dict["allergens"] = allergens

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_nutriments_dto import ArticleNutrimentsDto  # noqa: PLC0415

        d = dict(src_dict)
        _nutriments = d.pop("nutriments", UNSET)
        nutriments: ArticleNutrimentsDto | Unset
        if isinstance(_nutriments, Unset) or _nutriments is None:
            nutriments = UNSET
        else:
            nutriments = ArticleNutrimentsDto.from_dict(_nutriments)

        allergens = cast(list[str], d.pop("allergens", UNSET))

        parse_nutriments_result_dto = cls(
            nutriments=nutriments,
            allergens=allergens,
        )

        parse_nutriments_result_dto.additional_properties = d
        return parse_nutriments_result_dto

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
