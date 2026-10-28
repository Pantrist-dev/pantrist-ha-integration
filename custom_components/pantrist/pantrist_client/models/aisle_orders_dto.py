from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.aisle_order_dto import AisleOrderDto


T = TypeVar("T", bound="AisleOrdersDto")


@_attrs_define
class AisleOrdersDto:
    """
    Attributes:
        markets (list[AisleOrderDto]): One entry per market with timed purchases.
    """

    markets: list[AisleOrderDto]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        markets = []
        for markets_item_data in self.markets:
            markets_item = markets_item_data.to_dict()
            markets.append(markets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "markets": markets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aisle_order_dto import AisleOrderDto  # noqa: PLC0415

        d = dict(src_dict)
        markets = []
        _markets = d.pop("markets")
        for markets_item_data in _markets:
            markets_item = AisleOrderDto.from_dict(markets_item_data)

            markets.append(markets_item)

        aisle_orders_dto = cls(
            markets=markets,
        )

        aisle_orders_dto.additional_properties = d
        return aisle_orders_dto

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
