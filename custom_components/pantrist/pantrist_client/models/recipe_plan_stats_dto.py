from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="RecipePlanStatsDto")


@_attrs_define
class RecipePlanStatsDto:
    """
    Attributes:
        recipe_uuid (str): Recipe UUID the stats belong to
        times_planned (float): How often the recipe was planned in the past
        last_planned (None | str): Most recent past planned date (YYYY-MM-DD), null if never
    """

    recipe_uuid: str
    times_planned: float
    last_planned: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_uuid = self.recipe_uuid

        times_planned = self.times_planned

        last_planned: None | str
        last_planned = self.last_planned

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeUuid": recipe_uuid,
                "timesPlanned": times_planned,
                "lastPlanned": last_planned,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        recipe_uuid = d.pop("recipeUuid")

        times_planned = d.pop("timesPlanned")

        def _parse_last_planned(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        last_planned = _parse_last_planned(d.pop("lastPlanned"))

        recipe_plan_stats_dto = cls(
            recipe_uuid=recipe_uuid,
            times_planned=times_planned,
            last_planned=last_planned,
        )

        recipe_plan_stats_dto.additional_properties = d
        return recipe_plan_stats_dto

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
