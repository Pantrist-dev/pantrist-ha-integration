from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.store_dto_no_offers_reason import StoreDtoNoOffersReason
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.store_dto_opening_hours import StoreDtoOpeningHours


T = TypeVar("T", bound="StoreDto")


@_attrs_define
class StoreDto:
    """
    Attributes:
        id (str): Pantrist store id — stable across imports.
        retailer_key (str): Chain key, e.g. "lidl".
        retailer_name (str): Chain display name, e.g. "Lidl".
        name (str):
        latitude (float): WGS84 latitude.
        longitude (float): WGS84 longitude.
        street (str | Unset):
        zip_ (str | Unset):
        city (str | Unset):
        distance_meters (float | Unset): Distance to the queried point in metres. Only set by the nearby search.
        opening_hours (StoreDtoOpeningHours | Unset): Opening hours as published by the chain, unnormalised.
        no_offers_reason (StoreDtoNoOffersReason | Unset): Set when the market is shown without offers because no source
            carries its region. The app greys it out and explains it per chain.
        external_offers_url (str | Unset): Where the chain shows this market's offers itself. Only set together with
            noOffersReason.
    """

    id: str
    retailer_key: str
    retailer_name: str
    name: str
    latitude: float
    longitude: float
    street: str | Unset = UNSET
    zip_: str | Unset = UNSET
    city: str | Unset = UNSET
    distance_meters: float | Unset = UNSET
    opening_hours: StoreDtoOpeningHours | Unset = UNSET
    no_offers_reason: StoreDtoNoOffersReason | Unset = UNSET
    external_offers_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        retailer_key = self.retailer_key

        retailer_name = self.retailer_name

        name = self.name

        latitude = self.latitude

        longitude = self.longitude

        street = self.street

        zip_ = self.zip_

        city = self.city

        distance_meters = self.distance_meters

        opening_hours: dict[str, Any] | Unset = UNSET
        if not isinstance(self.opening_hours, Unset):
            opening_hours = self.opening_hours.to_dict()

        no_offers_reason: str | Unset = UNSET
        if not isinstance(self.no_offers_reason, Unset):
            no_offers_reason = self.no_offers_reason.value

        external_offers_url = self.external_offers_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "retailerKey": retailer_key,
                "retailerName": retailer_name,
                "name": name,
                "latitude": latitude,
                "longitude": longitude,
            }
        )
        if street is not UNSET:
            field_dict["street"] = street
        if zip_ is not UNSET:
            field_dict["zip"] = zip_
        if city is not UNSET:
            field_dict["city"] = city
        if distance_meters is not UNSET:
            field_dict["distanceMeters"] = distance_meters
        if opening_hours is not UNSET:
            field_dict["openingHours"] = opening_hours
        if no_offers_reason is not UNSET:
            field_dict["noOffersReason"] = no_offers_reason
        if external_offers_url is not UNSET:
            field_dict["externalOffersUrl"] = external_offers_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.store_dto_opening_hours import StoreDtoOpeningHours  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        retailer_key = d.pop("retailerKey")

        retailer_name = d.pop("retailerName")

        name = d.pop("name")

        latitude = d.pop("latitude")

        longitude = d.pop("longitude")

        street = d.pop("street", UNSET)

        zip_ = d.pop("zip", UNSET)

        city = d.pop("city", UNSET)

        distance_meters = d.pop("distanceMeters", UNSET)

        _opening_hours = d.pop("openingHours", UNSET)
        opening_hours: StoreDtoOpeningHours | Unset
        if isinstance(_opening_hours, Unset) or _opening_hours is None:
            opening_hours = UNSET
        else:
            opening_hours = StoreDtoOpeningHours.from_dict(_opening_hours)

        _no_offers_reason = d.pop("noOffersReason", UNSET)
        no_offers_reason: StoreDtoNoOffersReason | Unset
        if isinstance(_no_offers_reason, Unset) or _no_offers_reason is None or _no_offers_reason == "":
            no_offers_reason = UNSET
        else:
            no_offers_reason = StoreDtoNoOffersReason(_no_offers_reason)

        external_offers_url = d.pop("externalOffersUrl", UNSET)

        store_dto = cls(
            id=id,
            retailer_key=retailer_key,
            retailer_name=retailer_name,
            name=name,
            latitude=latitude,
            longitude=longitude,
            street=street,
            zip_=zip_,
            city=city,
            distance_meters=distance_meters,
            opening_hours=opening_hours,
            no_offers_reason=no_offers_reason,
            external_offers_url=external_offers_url,
        )

        store_dto.additional_properties = d
        return store_dto

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
