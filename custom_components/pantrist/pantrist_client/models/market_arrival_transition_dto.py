from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.market_arrival_transition_dto_transition import MarketArrivalTransitionDtoTransition
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.market_arrival_payload_dto import MarketArrivalPayloadDto


T = TypeVar("T", bound="MarketArrivalTransitionDto")


@_attrs_define
class MarketArrivalTransitionDto:
    """
    Attributes:
        identifier (str): Region identifier set by the app
        transition (MarketArrivalTransitionDtoTransition):
        enter (bool | Unset):
        payload (MarketArrivalPayloadDto | Unset):
    """

    identifier: str
    transition: MarketArrivalTransitionDtoTransition
    enter: bool | Unset = UNSET
    payload: MarketArrivalPayloadDto | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        identifier = self.identifier

        transition = self.transition.value

        enter = self.enter

        payload: dict[str, Any] | Unset = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "identifier": identifier,
                "transition": transition,
            }
        )
        if enter is not UNSET:
            field_dict["enter"] = enter
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.market_arrival_payload_dto import MarketArrivalPayloadDto  # noqa: PLC0415

        d = dict(src_dict)
        identifier = d.pop("identifier")

        transition = MarketArrivalTransitionDtoTransition(d.pop("transition"))

        enter = d.pop("enter", UNSET)

        _payload = d.pop("payload", UNSET)
        payload: MarketArrivalPayloadDto | Unset
        if isinstance(_payload, Unset) or _payload is None:
            payload = UNSET
        else:
            payload = MarketArrivalPayloadDto.from_dict(_payload)

        market_arrival_transition_dto = cls(
            identifier=identifier,
            transition=transition,
            enter=enter,
            payload=payload,
        )

        market_arrival_transition_dto.additional_properties = d
        return market_arrival_transition_dto

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
