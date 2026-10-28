from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.store_offers_dto_no_offers_reason import StoreOffersDtoNoOffersReason
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offer_dto import OfferDto


T = TypeVar("T", bound="StoreOffersDto")


@_attrs_define
class StoreOffersDto:
    """
    Attributes:
        store_id (str):
        retailer_key (str):
        store_name (str):
        latitude (float):
        longitude (float):
        offers (list[OfferDto]):
        no_offers_reason (StoreOffersDtoNoOffersReason | Unset): Set when the market is shown without offers because no
            source carries its region. The app greys it out and explains it per chain.
        external_offers_url (str | Unset): Where the chain shows this market's offers itself. Only set together with
            noOffersReason.
    """

    store_id: str
    retailer_key: str
    store_name: str
    latitude: float
    longitude: float
    offers: list[OfferDto]
    no_offers_reason: StoreOffersDtoNoOffersReason | Unset = UNSET
    external_offers_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        store_id = self.store_id

        retailer_key = self.retailer_key

        store_name = self.store_name

        latitude = self.latitude

        longitude = self.longitude

        offers = []
        for offers_item_data in self.offers:
            offers_item = offers_item_data.to_dict()
            offers.append(offers_item)

        no_offers_reason: str | Unset = UNSET
        if not isinstance(self.no_offers_reason, Unset):
            no_offers_reason = self.no_offers_reason.value

        external_offers_url = self.external_offers_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "storeId": store_id,
                "retailerKey": retailer_key,
                "storeName": store_name,
                "latitude": latitude,
                "longitude": longitude,
                "offers": offers,
            }
        )
        if no_offers_reason is not UNSET:
            field_dict["noOffersReason"] = no_offers_reason
        if external_offers_url is not UNSET:
            field_dict["externalOffersUrl"] = external_offers_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offer_dto import OfferDto  # noqa: PLC0415

        d = dict(src_dict)
        store_id = d.pop("storeId")

        retailer_key = d.pop("retailerKey")

        store_name = d.pop("storeName")

        latitude = d.pop("latitude")

        longitude = d.pop("longitude")

        offers = []
        _offers = d.pop("offers")
        for offers_item_data in _offers:
            offers_item = OfferDto.from_dict(offers_item_data)

            offers.append(offers_item)

        _no_offers_reason = d.pop("noOffersReason", UNSET)
        no_offers_reason: StoreOffersDtoNoOffersReason | Unset
        if isinstance(_no_offers_reason, Unset) or _no_offers_reason is None or _no_offers_reason == "":
            no_offers_reason = UNSET
        else:
            no_offers_reason = StoreOffersDtoNoOffersReason(_no_offers_reason)

        external_offers_url = d.pop("externalOffersUrl", UNSET)

        store_offers_dto = cls(
            store_id=store_id,
            retailer_key=retailer_key,
            store_name=store_name,
            latitude=latitude,
            longitude=longitude,
            offers=offers,
            no_offers_reason=no_offers_reason,
            external_offers_url=external_offers_url,
        )

        store_offers_dto.additional_properties = d
        return store_offers_dto

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
