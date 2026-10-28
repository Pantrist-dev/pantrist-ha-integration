from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offer_dto import OfferDto
    from ..models.store_dto import StoreDto


T = TypeVar("T", bound="OfferSearchResultDto")


@_attrs_define
class OfferSearchResultDto:
    """
    Attributes:
        store (StoreDto):
        matching_offers (list[OfferDto]): Only the offers at this store matching the search text — not the full catalog
            (see findOffersForStore for that).
    """

    store: StoreDto
    matching_offers: list[OfferDto]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        store = self.store.to_dict()

        matching_offers = []
        for matching_offers_item_data in self.matching_offers:
            matching_offers_item = matching_offers_item_data.to_dict()
            matching_offers.append(matching_offers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "store": store,
                "matchingOffers": matching_offers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offer_dto import OfferDto  # noqa: PLC0415
        from ..models.store_dto import StoreDto  # noqa: PLC0415

        d = dict(src_dict)
        store = StoreDto.from_dict(d.pop("store"))

        matching_offers = []
        _matching_offers = d.pop("matchingOffers")
        for matching_offers_item_data in _matching_offers:
            matching_offers_item = OfferDto.from_dict(matching_offers_item_data)

            matching_offers.append(matching_offers_item)

        offer_search_result_dto = cls(
            store=store,
            matching_offers=matching_offers,
        )

        offer_search_result_dto.additional_properties = d
        return offer_search_result_dto

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
