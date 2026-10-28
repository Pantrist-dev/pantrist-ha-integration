from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.category_item_type import CategoryItemType
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
        item_type (CategoryItemType | Unset): 'non-food' when the category is non-food in any of the lists merged into
            this entry; absent means food.
        default_best_before_days (float | None | Unset):
        complex_best_before_data (ArticleCatalogBestBeforeDatesDto | Unset):
        manage_minimum_stock (bool | Unset): When true, this category takes part in the minimum-stock rule: the server
            keeps a placeholder item on the shopping list for as long as the pantry holds less of this category than
            `minimumStock`. Omitted or false means the category is not managed.
        minimum_stock (float | None | Unset): How much of this category the household wants to keep in the pantry,
            measured as the summed `amount` of its pantry items. Only applied while `manageMinimumStock` is true.
    """

    uuid: str
    name: CategoryDtoNameType1 | str
    color: str | Unset = UNSET
    item_type: CategoryItemType | Unset = UNSET
    default_best_before_days: float | None | Unset = UNSET
    complex_best_before_data: ArticleCatalogBestBeforeDatesDto | Unset = UNSET
    manage_minimum_stock: bool | Unset = UNSET
    minimum_stock: float | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.category_dto_name_type_1 import CategoryDtoNameType1  # noqa: PLC0415

        uuid = self.uuid

        name: dict[str, Any] | str
        if isinstance(self.name, CategoryDtoNameType1):
            name = self.name.to_dict()
        else:
            name = self.name

        color = self.color

        item_type: str | Unset = UNSET
        if not isinstance(self.item_type, Unset):
            item_type = self.item_type.value

        default_best_before_days: float | None | Unset
        if isinstance(self.default_best_before_days, Unset):
            default_best_before_days = UNSET
        else:
            default_best_before_days = self.default_best_before_days

        complex_best_before_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.complex_best_before_data, Unset):
            complex_best_before_data = self.complex_best_before_data.to_dict()

        manage_minimum_stock = self.manage_minimum_stock

        minimum_stock: float | None | Unset
        if isinstance(self.minimum_stock, Unset):
            minimum_stock = UNSET
        else:
            minimum_stock = self.minimum_stock

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
        if item_type is not UNSET:
            field_dict["itemType"] = item_type
        if default_best_before_days is not UNSET:
            field_dict["defaultBestBeforeDays"] = default_best_before_days
        if complex_best_before_data is not UNSET:
            field_dict["complexBestBeforeData"] = complex_best_before_data
        if manage_minimum_stock is not UNSET:
            field_dict["manageMinimumStock"] = manage_minimum_stock
        if minimum_stock is not UNSET:
            field_dict["minimumStock"] = minimum_stock

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto  # noqa: PLC0415
        from ..models.category_dto_name_type_1 import CategoryDtoNameType1  # noqa: PLC0415

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

        _item_type = d.pop("itemType", UNSET)
        item_type: CategoryItemType | Unset
        if isinstance(_item_type, Unset) or _item_type is None or _item_type == "":
            item_type = UNSET
        else:
            item_type = CategoryItemType(_item_type)

        def _parse_default_best_before_days(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        default_best_before_days = _parse_default_best_before_days(d.pop("defaultBestBeforeDays", UNSET))

        _complex_best_before_data = d.pop("complexBestBeforeData", UNSET)
        complex_best_before_data: ArticleCatalogBestBeforeDatesDto | Unset
        if isinstance(_complex_best_before_data, Unset) or _complex_best_before_data is None:
            complex_best_before_data = UNSET
        else:
            complex_best_before_data = ArticleCatalogBestBeforeDatesDto.from_dict(_complex_best_before_data)

        manage_minimum_stock = d.pop("manageMinimumStock", UNSET)

        def _parse_minimum_stock(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        minimum_stock = _parse_minimum_stock(d.pop("minimumStock", UNSET))

        category_dto = cls(
            uuid=uuid,
            name=name,
            color=color,
            item_type=item_type,
            default_best_before_days=default_best_before_days,
            complex_best_before_data=complex_best_before_data,
            manage_minimum_stock=manage_minimum_stock,
            minimum_stock=minimum_stock,
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
