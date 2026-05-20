from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.merged_category_dto_list_category_ids import MergedCategoryDtoListCategoryIds
    from ..models.merged_category_dto_name_type_1 import MergedCategoryDtoNameType1


T = TypeVar("T", bound="MergedCategoryDto")


@_attrs_define
class MergedCategoryDto:
    """
    Attributes:
        name (MergedCategoryDtoNameType1 | str): Either a plain string or a translation key object
        list_category_ids (MergedCategoryDtoListCategoryIds): Map of listId → categoryUuid
        color (str | Unset):
        default_best_before_days (float | None | Unset):
    """

    name: MergedCategoryDtoNameType1 | str
    list_category_ids: MergedCategoryDtoListCategoryIds
    color: str | Unset = UNSET
    default_best_before_days: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.merged_category_dto_name_type_1 import MergedCategoryDtoNameType1

        name: dict[str, Any] | str
        if isinstance(self.name, MergedCategoryDtoNameType1):
            name = self.name.to_dict()
        else:
            name = self.name

        list_category_ids = self.list_category_ids.to_dict()

        color = self.color

        default_best_before_days: float | None | Unset
        if isinstance(self.default_best_before_days, Unset):
            default_best_before_days = UNSET
        else:
            default_best_before_days = self.default_best_before_days

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "listCategoryIds": list_category_ids,
            }
        )
        if color is not UNSET:
            field_dict["color"] = color
        if default_best_before_days is not UNSET:
            field_dict["defaultBestBeforeDays"] = default_best_before_days

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.merged_category_dto_list_category_ids import MergedCategoryDtoListCategoryIds
        from ..models.merged_category_dto_name_type_1 import MergedCategoryDtoNameType1

        d = dict(src_dict)

        def _parse_name(data: object) -> MergedCategoryDtoNameType1 | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                name_type_1 = MergedCategoryDtoNameType1.from_dict(data)

                return name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(MergedCategoryDtoNameType1 | str, data)

        name = _parse_name(d.pop("name"))

        list_category_ids = MergedCategoryDtoListCategoryIds.from_dict(d.pop("listCategoryIds"))

        color = d.pop("color", UNSET)

        def _parse_default_best_before_days(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        default_best_before_days = _parse_default_best_before_days(d.pop("defaultBestBeforeDays", UNSET))

        merged_category_dto = cls(
            name=name,
            list_category_ids=list_category_ids,
            color=color,
            default_best_before_days=default_best_before_days,
        )

        merged_category_dto.additional_properties = d
        return merged_category_dto

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
