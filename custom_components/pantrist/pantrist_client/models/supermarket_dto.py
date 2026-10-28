from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.linked_store_dto import LinkedStoreDto


T = TypeVar("T", bound="SupermarketDto")


@_attrs_define
class SupermarketDto:
    """
    Attributes:
        uid (str):
        name (str):
        icon_id (str):
        category_sort_order (list[str] | None | Unset):
        different_order (bool | None | Unset):
        retailer_key (None | str | Unset): Chain identifier (e.g. "rewe") when a default-supermarket icon was picked,
            null for a custom market.
        store_id (None | str | Unset): The real branch (offers module store id) this market is, if the user linked one.
            Unlike retailerKey, identifies a specific location, not just the chain.
        linked_store (LinkedStoreDto | Unset):
        geofence_lat (float | None | Unset): Geofence centre latitude (decimal degrees)
        geofence_lng (float | None | Unset): Geofence centre longitude (decimal degrees)
        geofence_radius_m (float | None | Unset): Geofence radius in metres
        geofence_captured_at (None | str | Unset): When the geofence was captured (ISO 8601)
        geofence_address (None | str | Unset): Address of the geofence centre, shown to the user in place of
            coordinates. Display only: arrival is decided by the coordinates.
    """

    uid: str
    name: str
    icon_id: str
    category_sort_order: list[str] | None | Unset = UNSET
    different_order: bool | None | Unset = UNSET
    retailer_key: None | str | Unset = UNSET
    store_id: None | str | Unset = UNSET
    linked_store: LinkedStoreDto | Unset = UNSET
    geofence_lat: float | None | Unset = UNSET
    geofence_lng: float | None | Unset = UNSET
    geofence_radius_m: float | None | Unset = UNSET
    geofence_captured_at: None | str | Unset = UNSET
    geofence_address: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uid = self.uid

        name = self.name

        icon_id = self.icon_id

        category_sort_order: list[str] | None | Unset
        if isinstance(self.category_sort_order, Unset):
            category_sort_order = UNSET
        elif isinstance(self.category_sort_order, list):
            category_sort_order = self.category_sort_order

        else:
            category_sort_order = self.category_sort_order

        different_order: bool | None | Unset
        if isinstance(self.different_order, Unset):
            different_order = UNSET
        else:
            different_order = self.different_order

        retailer_key: None | str | Unset
        if isinstance(self.retailer_key, Unset):
            retailer_key = UNSET
        else:
            retailer_key = self.retailer_key

        store_id: None | str | Unset
        if isinstance(self.store_id, Unset):
            store_id = UNSET
        else:
            store_id = self.store_id

        linked_store: dict[str, Any] | Unset = UNSET
        if not isinstance(self.linked_store, Unset):
            linked_store = self.linked_store.to_dict()

        geofence_lat: float | None | Unset
        if isinstance(self.geofence_lat, Unset):
            geofence_lat = UNSET
        else:
            geofence_lat = self.geofence_lat

        geofence_lng: float | None | Unset
        if isinstance(self.geofence_lng, Unset):
            geofence_lng = UNSET
        else:
            geofence_lng = self.geofence_lng

        geofence_radius_m: float | None | Unset
        if isinstance(self.geofence_radius_m, Unset):
            geofence_radius_m = UNSET
        else:
            geofence_radius_m = self.geofence_radius_m

        geofence_captured_at: None | str | Unset
        if isinstance(self.geofence_captured_at, Unset):
            geofence_captured_at = UNSET
        else:
            geofence_captured_at = self.geofence_captured_at

        geofence_address: None | str | Unset
        if isinstance(self.geofence_address, Unset):
            geofence_address = UNSET
        else:
            geofence_address = self.geofence_address

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uid": uid,
                "name": name,
                "iconId": icon_id,
            }
        )
        if category_sort_order is not UNSET:
            field_dict["categorySortOrder"] = category_sort_order
        if different_order is not UNSET:
            field_dict["differentOrder"] = different_order
        if retailer_key is not UNSET:
            field_dict["retailerKey"] = retailer_key
        if store_id is not UNSET:
            field_dict["storeId"] = store_id
        if linked_store is not UNSET:
            field_dict["linkedStore"] = linked_store
        if geofence_lat is not UNSET:
            field_dict["geofenceLat"] = geofence_lat
        if geofence_lng is not UNSET:
            field_dict["geofenceLng"] = geofence_lng
        if geofence_radius_m is not UNSET:
            field_dict["geofenceRadiusM"] = geofence_radius_m
        if geofence_captured_at is not UNSET:
            field_dict["geofenceCapturedAt"] = geofence_captured_at
        if geofence_address is not UNSET:
            field_dict["geofenceAddress"] = geofence_address

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.linked_store_dto import LinkedStoreDto  # noqa: PLC0415

        d = dict(src_dict)
        uid = d.pop("uid")

        name = d.pop("name")

        icon_id = d.pop("iconId")

        def _parse_category_sort_order(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                category_sort_order_type_0 = cast(list[str], data)

                return category_sort_order_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        category_sort_order = _parse_category_sort_order(d.pop("categorySortOrder", UNSET))

        def _parse_different_order(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        different_order = _parse_different_order(d.pop("differentOrder", UNSET))

        def _parse_retailer_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        retailer_key = _parse_retailer_key(d.pop("retailerKey", UNSET))

        def _parse_store_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        store_id = _parse_store_id(d.pop("storeId", UNSET))

        _linked_store = d.pop("linkedStore", UNSET)
        linked_store: LinkedStoreDto | Unset
        if isinstance(_linked_store, Unset) or _linked_store is None:
            linked_store = UNSET
        else:
            linked_store = LinkedStoreDto.from_dict(_linked_store)

        def _parse_geofence_lat(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        geofence_lat = _parse_geofence_lat(d.pop("geofenceLat", UNSET))

        def _parse_geofence_lng(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        geofence_lng = _parse_geofence_lng(d.pop("geofenceLng", UNSET))

        def _parse_geofence_radius_m(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        geofence_radius_m = _parse_geofence_radius_m(d.pop("geofenceRadiusM", UNSET))

        def _parse_geofence_captured_at(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        geofence_captured_at = _parse_geofence_captured_at(d.pop("geofenceCapturedAt", UNSET))

        def _parse_geofence_address(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        geofence_address = _parse_geofence_address(d.pop("geofenceAddress", UNSET))

        supermarket_dto = cls(
            uid=uid,
            name=name,
            icon_id=icon_id,
            category_sort_order=category_sort_order,
            different_order=different_order,
            retailer_key=retailer_key,
            store_id=store_id,
            linked_store=linked_store,
            geofence_lat=geofence_lat,
            geofence_lng=geofence_lng,
            geofence_radius_m=geofence_radius_m,
            geofence_captured_at=geofence_captured_at,
            geofence_address=geofence_address,
        )

        supermarket_dto.additional_properties = d
        return supermarket_dto

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
