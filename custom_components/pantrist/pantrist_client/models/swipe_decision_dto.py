from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.swipe_decision_dto_decision import SwipeDecisionDtoDecision
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.swipe_week_plan_target_dto import SwipeWeekPlanTargetDto


T = TypeVar("T", bound="SwipeDecisionDto")


@_attrs_define
class SwipeDecisionDto:
    """
    Attributes:
        recipe_uuid (str): UUID of the swiped recipe
        decision (SwipeDecisionDtoDecision): 'like' (swipe right) or 'skip' (swipe left)
        week_plan (SwipeWeekPlanTargetDto | Unset):
    """

    recipe_uuid: str
    decision: SwipeDecisionDtoDecision
    week_plan: SwipeWeekPlanTargetDto | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        recipe_uuid = self.recipe_uuid

        decision = self.decision.value

        week_plan: dict[str, Any] | Unset = UNSET
        if not isinstance(self.week_plan, Unset):
            week_plan = self.week_plan.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "recipeUuid": recipe_uuid,
                "decision": decision,
            }
        )
        if week_plan is not UNSET:
            field_dict["weekPlan"] = week_plan

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.swipe_week_plan_target_dto import SwipeWeekPlanTargetDto  # noqa: PLC0415

        d = dict(src_dict)
        recipe_uuid = d.pop("recipeUuid")

        decision = SwipeDecisionDtoDecision(d.pop("decision"))

        _week_plan = d.pop("weekPlan", UNSET)
        week_plan: SwipeWeekPlanTargetDto | Unset
        if isinstance(_week_plan, Unset) or _week_plan is None:
            week_plan = UNSET
        else:
            week_plan = SwipeWeekPlanTargetDto.from_dict(_week_plan)

        swipe_decision_dto = cls(
            recipe_uuid=recipe_uuid,
            decision=decision,
            week_plan=week_plan,
        )

        swipe_decision_dto.additional_properties = d
        return swipe_decision_dto

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
