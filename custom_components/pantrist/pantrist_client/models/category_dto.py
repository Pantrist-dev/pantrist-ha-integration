from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto
    from ..models.category_dto_name_type_1 import CategoryDtoNameType1


T = TypeVar("T", bound="CategoryDto")


@_attrs_define
class CategoryDto:
    """
    Attributes:
        uuid (str):
        name (CategoryDtoNameType1 | str): Either a plain string or a translation key object
        color (str | Unset):
        default_best_before_days (float | None | Unset):
        complex_best_before_data (ArticleCatalogBestBeforeDatesDto | Unset):
    """

    uuid: str
    name: CategoryDtoNameType1 | str
    color: str | Unset = UNSET
    default_best_before_days: float | None | Unset = UNSET
    complex_best_before_data: ArticleCatalogBestBeforeDatesDto | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.category_dto_name_type_1 import CategoryDtoNameType1

        uuid = self.uuid

        name: dict[str, Any] | str
        if isinstance(self.name, CategoryDtoNameType1):
            name = self.name.to_dict()
        else:
            name = self.name

        color = self.color

        default_best_before_days: float | None | Unset
        if isinstance(self.default_best_before_days, Unset):
            default_best_before_days = UNSET
        else:
            default_best_before_days = self.default_best_before_days

        complex_best_before_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.complex_best_before_data, Unset):
            complex_best_before_data = self.complex_best_before_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
            }
        )
        if color is not UNSET:
            field_dict["color"] = color
        if default_best_before_days is not UNSET:
            field_dict["defaultBestBeforeDays"] = default_best_before_days
        if complex_best_before_data is not UNSET:
            field_dict["complexBestBeforeData"] = complex_best_before_data

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto
        from ..models.category_dto_name_type_1 import CategoryDtoNameType1

        d = dict(src_dict)
        uuid = d.pop("uuid")

        def _parse_name(data: object) -> CategoryDtoNameType1 | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                name_type_1 = CategoryDtoNameType1.from_dict(data)

                return name_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CategoryDtoNameType1 | str, data)

        name = _parse_name(d.pop("name"))

        color = d.pop("color", UNSET)

        def _parse_default_best_before_days(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        default_best_before_days = _parse_default_best_before_days(d.pop("defaultBestBeforeDays", UNSET))

        _complex_best_before_data = d.pop("complexBestBeforeData", UNSET)
        complex_best_before_data: ArticleCatalogBestBeforeDatesDto | Unset
        if isinstance(_complex_best_before_data, Unset):
            complex_best_before_data = UNSET
        else:
            complex_best_before_data = ArticleCatalogBestBeforeDatesDto.from_dict(_complex_best_before_data)

        category_dto = cls(
            uuid=uuid,
            name=name,
            color=color,
            default_best_before_days=default_best_before_days,
            complex_best_before_data=complex_best_before_data,
        )

        category_dto.additional_properties = d
        return category_dto

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
