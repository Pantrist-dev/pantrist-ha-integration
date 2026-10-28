from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="HouseholdDetailsDto")


@_attrs_define
class HouseholdDetailsDto:
    """
    Attributes:
        manufacturer (None | str | Unset):
        model_number (None | str | Unset):
        serial_number (None | str | Unset):
        warranty_expiration (datetime.date | None | Unset): Last day of the warranty, YYYY-MM-DD.
        manual_url (None | str | Unset): Link to the manual or product page.
        purchase_source (None | str | Unset): Where the item was bought (shop, website).
    """

    manufacturer: None | str | Unset = UNSET
    model_number: None | str | Unset = UNSET
    serial_number: None | str | Unset = UNSET
    warranty_expiration: datetime.date | None | Unset = UNSET
    manual_url: None | str | Unset = UNSET
    purchase_source: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        manufacturer: None | str | Unset
        if isinstance(self.manufacturer, Unset):
            manufacturer = UNSET
        else:
            manufacturer = self.manufacturer

        model_number: None | str | Unset
        if isinstance(self.model_number, Unset):
            model_number = UNSET
        else:
            model_number = self.model_number

        serial_number: None | str | Unset
        if isinstance(self.serial_number, Unset):
            serial_number = UNSET
        else:
            serial_number = self.serial_number

        warranty_expiration: None | str | Unset
        if isinstance(self.warranty_expiration, Unset):
            warranty_expiration = UNSET
        elif isinstance(self.warranty_expiration, datetime.date):
            warranty_expiration = self.warranty_expiration.isoformat()
        else:
            warranty_expiration = self.warranty_expiration

        manual_url: None | str | Unset
        if isinstance(self.manual_url, Unset):
            manual_url = UNSET
        else:
            manual_url = self.manual_url

        purchase_source: None | str | Unset
        if isinstance(self.purchase_source, Unset):
            purchase_source = UNSET
        else:
            purchase_source = self.purchase_source

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if manufacturer is not UNSET:
            field_dict["manufacturer"] = manufacturer
        if model_number is not UNSET:
            field_dict["modelNumber"] = model_number
        if serial_number is not UNSET:
            field_dict["serialNumber"] = serial_number
        if warranty_expiration is not UNSET:
            field_dict["warrantyExpiration"] = warranty_expiration
        if manual_url is not UNSET:
            field_dict["manualUrl"] = manual_url
        if purchase_source is not UNSET:
            field_dict["purchaseSource"] = purchase_source

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_manufacturer(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        manufacturer = _parse_manufacturer(d.pop("manufacturer", UNSET))

        def _parse_model_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        model_number = _parse_model_number(d.pop("modelNumber", UNSET))

        def _parse_serial_number(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        serial_number = _parse_serial_number(d.pop("serialNumber", UNSET))

        def _parse_warranty_expiration(data: object) -> datetime.date | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                warranty_expiration_type_0 = datetime.date.fromisoformat(data)

                return warranty_expiration_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.date | None | Unset, data)

        warranty_expiration = _parse_warranty_expiration(d.pop("warrantyExpiration", UNSET))

        def _parse_manual_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        manual_url = _parse_manual_url(d.pop("manualUrl", UNSET))

        def _parse_purchase_source(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        purchase_source = _parse_purchase_source(d.pop("purchaseSource", UNSET))

        household_details_dto = cls(
            manufacturer=manufacturer,
            model_number=model_number,
            serial_number=serial_number,
            warranty_expiration=warranty_expiration,
            manual_url=manual_url,
            purchase_source=purchase_source,
        )

        household_details_dto.additional_properties = d
        return household_details_dto

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
