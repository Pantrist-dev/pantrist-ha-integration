from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.aisle_order_dto_confidence import AisleOrderDtoConfidence

if TYPE_CHECKING:
    from ..models.aisle_rank_dto import AisleRankDto


T = TypeVar("T", bound="AisleOrderDto")


@_attrs_define
class AisleOrderDto:
    """
    Attributes:
        market_id (str):
        confidence (AisleOrderDtoConfidence): 'high' from 3 trips and 5 distinct categories on; clients should keep
            their manual order while it is 'low'.
        trips (float): Trips the order was learned from.
        categories (list[AisleRankDto]): Categories, earliest in the market first.
        products (list[AisleRankDto]): Products, earliest in the market first.
    """

    market_id: str
    confidence: AisleOrderDtoConfidence
    trips: float
    categories: list[AisleRankDto]
    products: list[AisleRankDto]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        market_id = self.market_id

        confidence = self.confidence.value

        trips = self.trips

        categories = []
        for categories_item_data in self.categories:
            categories_item = categories_item_data.to_dict()
            categories.append(categories_item)

        products = []
        for products_item_data in self.products:
            products_item = products_item_data.to_dict()
            products.append(products_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "marketId": market_id,
                "confidence": confidence,
                "trips": trips,
                "categories": categories,
                "products": products,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.aisle_rank_dto import AisleRankDto  # noqa: PLC0415

        d = dict(src_dict)
        market_id = d.pop("marketId")

        confidence = AisleOrderDtoConfidence(d.pop("confidence"))

        trips = d.pop("trips")

        categories = []
        _categories = d.pop("categories")
        for categories_item_data in _categories:
            categories_item = AisleRankDto.from_dict(categories_item_data)

            categories.append(categories_item)

        products = []
        _products = d.pop("products")
        for products_item_data in _products:
            products_item = AisleRankDto.from_dict(products_item_data)

            products.append(products_item)

        aisle_order_dto = cls(
            market_id=market_id,
            confidence=confidence,
            trips=trips,
            categories=categories,
            products=products,
        )

        aisle_order_dto.additional_properties = d
        return aisle_order_dto

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
