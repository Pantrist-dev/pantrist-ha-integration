from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.value_with_metric_and_opening_dto import ValueWithMetricAndOpeningDto


T = TypeVar("T", bound="ArticleCatalogBestBeforeDatesDto")


@_attrs_define
class ArticleCatalogBestBeforeDatesDto:
    """
    Attributes:
        pantry (ValueWithMetricAndOpeningDto | Unset):
        refrigerate (ValueWithMetricAndOpeningDto | Unset):
        freeze (ValueWithMetricAndOpeningDto | Unset):
    """

    pantry: ValueWithMetricAndOpeningDto | Unset = UNSET
    refrigerate: ValueWithMetricAndOpeningDto | Unset = UNSET
    freeze: ValueWithMetricAndOpeningDto | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pantry: dict[str, Any] | Unset = UNSET
        if not isinstance(self.pantry, Unset):
            pantry = self.pantry.to_dict()

        refrigerate: dict[str, Any] | Unset = UNSET
        if not isinstance(self.refrigerate, Unset):
            refrigerate = self.refrigerate.to_dict()

        freeze: dict[str, Any] | Unset = UNSET
        if not isinstance(self.freeze, Unset):
            freeze = self.freeze.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pantry is not UNSET:
            field_dict["pantry"] = pantry
        if refrigerate is not UNSET:
            field_dict["refrigerate"] = refrigerate
        if freeze is not UNSET:
            field_dict["freeze"] = freeze

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.value_with_metric_and_opening_dto import ValueWithMetricAndOpeningDto

        d = dict(src_dict)
        _pantry = d.pop("pantry", UNSET)
        pantry: ValueWithMetricAndOpeningDto | Unset
        if isinstance(_pantry, Unset):
            pantry = UNSET
        else:
            pantry = ValueWithMetricAndOpeningDto.from_dict(_pantry)

        _refrigerate = d.pop("refrigerate", UNSET)
        refrigerate: ValueWithMetricAndOpeningDto | Unset
        if isinstance(_refrigerate, Unset):
            refrigerate = UNSET
        else:
            refrigerate = ValueWithMetricAndOpeningDto.from_dict(_refrigerate)

        _freeze = d.pop("freeze", UNSET)
        freeze: ValueWithMetricAndOpeningDto | Unset
        if isinstance(_freeze, Unset):
            freeze = UNSET
        else:
            freeze = ValueWithMetricAndOpeningDto.from_dict(_freeze)

        article_catalog_best_before_dates_dto = cls(
            pantry=pantry,
            refrigerate=refrigerate,
            freeze=freeze,
        )

        article_catalog_best_before_dates_dto.additional_properties = d
        return article_catalog_best_before_dates_dto

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
