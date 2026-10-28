from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.auto_reduce_interval_dto import AutoReduceIntervalDto
    from ..models.auto_reduce_weekday_dto import AutoReduceWeekdayDto


T = TypeVar("T", bound="AutoReduceConfigDto")


@_attrs_define
class AutoReduceConfigDto:
    """
    Attributes:
        enabled (bool):
        schedule (AutoReduceIntervalDto | AutoReduceWeekdayDto | Unset): Required when `enabled` is true
        activated_at (str | Unset): ISO timestamp the user activated auto-reduce on this item. Stamped by the app on the
            false→true toggle and preserved across schedule edits. Accrual is clamped to `max(userCursor, activatedAt)` so a
            freshly-enabled item does not retroactively count consumption from before activation.
    """

    enabled: bool
    schedule: AutoReduceIntervalDto | AutoReduceWeekdayDto | Unset = UNSET
    activated_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.auto_reduce_interval_dto import AutoReduceIntervalDto  # noqa: PLC0415

        enabled = self.enabled

        schedule: dict[str, Any] | Unset
        if isinstance(self.schedule, Unset):
            schedule = UNSET
        elif isinstance(self.schedule, AutoReduceIntervalDto):
            schedule = self.schedule.to_dict()
        else:
            schedule = self.schedule.to_dict()

        activated_at = self.activated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
            }
        )
        if schedule is not UNSET:
            field_dict["schedule"] = schedule
        if activated_at is not UNSET:
            field_dict["activatedAt"] = activated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auto_reduce_interval_dto import AutoReduceIntervalDto  # noqa: PLC0415
        from ..models.auto_reduce_weekday_dto import AutoReduceWeekdayDto  # noqa: PLC0415

        d = dict(src_dict)
        enabled = d.pop("enabled")

        def _parse_schedule(data: object) -> AutoReduceIntervalDto | AutoReduceWeekdayDto | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                schedule_type_0 = AutoReduceIntervalDto.from_dict(data)

                return schedule_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            schedule_type_1 = AutoReduceWeekdayDto.from_dict(data)

            return schedule_type_1

        schedule = _parse_schedule(d.pop("schedule", UNSET))

        activated_at = d.pop("activatedAt", UNSET)

        auto_reduce_config_dto = cls(
            enabled=enabled,
            schedule=schedule,
            activated_at=activated_at,
        )

        auto_reduce_config_dto.additional_properties = d
        return auto_reduce_config_dto

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
