from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.value_with_metric_and_opening_dto_metric import ValueWithMetricAndOpeningDtoMetric
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.value_with_metric_dto import ValueWithMetricDto


T = TypeVar("T", bound="ValueWithMetricAndOpeningDto")


@_attrs_define
class ValueWithMetricAndOpeningDto:
    """
    Attributes:
        value (float | Unset):
        metric (ValueWithMetricAndOpeningDtoMetric | Unset):
        after_opening (ValueWithMetricDto | Unset):
    """

    value: float | Unset = UNSET
    metric: ValueWithMetricAndOpeningDtoMetric | Unset = UNSET
    after_opening: ValueWithMetricDto | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        metric: str | Unset = UNSET
        if not isinstance(self.metric, Unset):
            metric = self.metric.value

        after_opening: dict[str, Any] | Unset = UNSET
        if not isinstance(self.after_opening, Unset):
            after_opening = self.after_opening.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if metric is not UNSET:
            field_dict["metric"] = metric
        if after_opening is not UNSET:
            field_dict["afterOpening"] = after_opening

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.value_with_metric_dto import ValueWithMetricDto

        d = dict(src_dict)
        value = d.pop("value", UNSET)

        _metric = d.pop("metric", UNSET)
        metric: ValueWithMetricAndOpeningDtoMetric | Unset
        if isinstance(_metric, Unset):
            metric = UNSET
        else:
            metric = ValueWithMetricAndOpeningDtoMetric(_metric)

        _after_opening = d.pop("afterOpening", UNSET)
        after_opening: ValueWithMetricDto | Unset
        if isinstance(_after_opening, Unset):
            after_opening = UNSET
        else:
            after_opening = ValueWithMetricDto.from_dict(_after_opening)

        value_with_metric_and_opening_dto = cls(
            value=value,
            metric=metric,
            after_opening=after_opening,
        )

        value_with_metric_and_opening_dto.additional_properties = d
        return value_with_metric_and_opening_dto

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
