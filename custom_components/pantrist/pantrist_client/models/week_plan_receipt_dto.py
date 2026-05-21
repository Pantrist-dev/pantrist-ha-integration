from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.week_plan_receipt_dto_type import WeekPlanReceiptDtoType
from ..types import UNSET, Unset

T = TypeVar("T", bound="WeekPlanReceiptDto")


@_attrs_define
class WeekPlanReceiptDto:
    """
    Attributes:
        uuid (str | Unset): Recipe UUID (for type recipe)
        name (str | Unset): Manual name (for type manual)
        type_ (WeekPlanReceiptDtoType | Unset):
    """

    uuid: str | Unset = UNSET
    name: str | Unset = UNSET
    type_: WeekPlanReceiptDtoType | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        name = self.name

        type_: str | Unset = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid", UNSET)

        name = d.pop("name", UNSET)

        _type_ = d.pop("type", UNSET)
        type_: WeekPlanReceiptDtoType | Unset
        if isinstance(_type_, Unset) or _type_ is None or _type_ == "":
            type_ = UNSET
        else:
            type_ = WeekPlanReceiptDtoType(_type_)

        week_plan_receipt_dto = cls(
            uuid=uuid,
            name=name,
            type_=type_,
        )

        week_plan_receipt_dto.additional_properties = d
        return week_plan_receipt_dto

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
