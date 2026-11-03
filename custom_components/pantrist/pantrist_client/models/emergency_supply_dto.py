from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.emergency_supply_dto_standard import EmergencySupplyDtoStandard
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.emergency_supply_group_dto import EmergencySupplyGroupDto


T = TypeVar("T", bound="EmergencySupplyDto")


@_attrs_define
class EmergencySupplyDto:
    """
    Attributes:
        enabled (bool): False when the list switched the emergency supply off; `groups` is then empty.
        people_count (float): People the supply is counted for.
        food_weight (float): Weight of the food in the pantry in kg, over the list's food categories.
        groups (list[EmergencySupplyGroupDto]):
        standard (EmergencySupplyDtoStandard | Unset):
        days (float | None | Unset): How many days the whole supply lasts: as long as its scarcest group.
        scarcest_group (None | str | Unset): Id of the group that runs out first.
    """

    enabled: bool
    people_count: float
    food_weight: float
    groups: list[EmergencySupplyGroupDto]
    standard: EmergencySupplyDtoStandard | Unset = UNSET
    days: float | None | Unset = UNSET
    scarcest_group: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        enabled = self.enabled

        people_count = self.people_count

        food_weight = self.food_weight

        groups = []
        for groups_item_data in self.groups:
            groups_item = groups_item_data.to_dict()
            groups.append(groups_item)

        standard: str | Unset = UNSET
        if not isinstance(self.standard, Unset):
            standard = self.standard.value

        days: float | None | Unset
        if isinstance(self.days, Unset):
            days = UNSET
        else:
            days = self.days

        scarcest_group: None | str | Unset
        if isinstance(self.scarcest_group, Unset):
            scarcest_group = UNSET
        else:
            scarcest_group = self.scarcest_group

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "peopleCount": people_count,
                "foodWeight": food_weight,
                "groups": groups,
            }
        )
        if standard is not UNSET:
            field_dict["standard"] = standard
        if days is not UNSET:
            field_dict["days"] = days
        if scarcest_group is not UNSET:
            field_dict["scarcestGroup"] = scarcest_group

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.emergency_supply_group_dto import EmergencySupplyGroupDto  # noqa: PLC0415

        d = dict(src_dict)
        enabled = d.pop("enabled")

        people_count = d.pop("peopleCount")

        food_weight = d.pop("foodWeight")

        groups = []
        _groups = d.pop("groups")
        for groups_item_data in _groups:
            groups_item = EmergencySupplyGroupDto.from_dict(groups_item_data)

            groups.append(groups_item)

        _standard = d.pop("standard", UNSET)
        standard: EmergencySupplyDtoStandard | Unset
        if isinstance(_standard, Unset) or _standard is None or _standard == "":
            standard = UNSET
        else:
            standard = EmergencySupplyDtoStandard(_standard)

        def _parse_days(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        days = _parse_days(d.pop("days", UNSET))

        def _parse_scarcest_group(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        scarcest_group = _parse_scarcest_group(d.pop("scarcestGroup", UNSET))

        emergency_supply_dto = cls(
            enabled=enabled,
            people_count=people_count,
            food_weight=food_weight,
            groups=groups,
            standard=standard,
            days=days,
            scarcest_group=scarcest_group,
        )

        emergency_supply_dto.additional_properties = d
        return emergency_supply_dto

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
