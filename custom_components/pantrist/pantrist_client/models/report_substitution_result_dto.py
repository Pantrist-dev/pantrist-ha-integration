from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.report_substitution_result_dto_status import ReportSubstitutionResultDtoStatus

T = TypeVar("T", bound="ReportSubstitutionResultDto")


@_attrs_define
class ReportSubstitutionResultDto:
    """
    Attributes:
        report_count (float): Distinct users who reported this substitution so far.
        status (ReportSubstitutionResultDtoStatus): Lifecycle after this report. `disabled` means the hint will no
            longer be shown to anyone.
    """

    report_count: float
    status: ReportSubstitutionResultDtoStatus
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        report_count = self.report_count

        status = self.status.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "reportCount": report_count,
                "status": status,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        report_count = d.pop("reportCount")

        status = ReportSubstitutionResultDtoStatus(d.pop("status"))

        report_substitution_result_dto = cls(
            report_count=report_count,
            status=status,
        )

        report_substitution_result_dto.additional_properties = d
        return report_substitution_result_dto

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
