from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.buy_reminder_row_dto_confidence import BuyReminderRowDtoConfidence

if TYPE_CHECKING:
    from ..models.buy_reminder_last_purchase_dto import BuyReminderLastPurchaseDto


T = TypeVar("T", bound="BuyReminderRowDto")


@_attrs_define
class BuyReminderRowDto:
    """
    Attributes:
        identity_key (str):
        display_name (str):
        brand (None | str):
        barcode (None | str):
        last_purchase_at (str):
        typical_interval_days (float):
        days_since_last_purchase (float):
        confidence (BuyReminderRowDtoConfidence):
        last_purchase (BuyReminderLastPurchaseDto):
    """

    identity_key: str
    display_name: str
    brand: None | str
    barcode: None | str
    last_purchase_at: str
    typical_interval_days: float
    days_since_last_purchase: float
    confidence: BuyReminderRowDtoConfidence
    last_purchase: BuyReminderLastPurchaseDto
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        identity_key = self.identity_key

        display_name = self.display_name

        brand: None | str
        brand = self.brand

        barcode: None | str
        barcode = self.barcode

        last_purchase_at = self.last_purchase_at

        typical_interval_days = self.typical_interval_days

        days_since_last_purchase = self.days_since_last_purchase

        confidence = self.confidence.value

        last_purchase = self.last_purchase.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "identityKey": identity_key,
                "displayName": display_name,
                "brand": brand,
                "barcode": barcode,
                "lastPurchaseAt": last_purchase_at,
                "typicalIntervalDays": typical_interval_days,
                "daysSinceLastPurchase": days_since_last_purchase,
                "confidence": confidence,
                "lastPurchase": last_purchase,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.buy_reminder_last_purchase_dto import BuyReminderLastPurchaseDto  # noqa: PLC0415

        d = dict(src_dict)
        identity_key = d.pop("identityKey")

        display_name = d.pop("displayName")

        def _parse_brand(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        brand = _parse_brand(d.pop("brand"))

        def _parse_barcode(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        barcode = _parse_barcode(d.pop("barcode"))

        last_purchase_at = d.pop("lastPurchaseAt")

        typical_interval_days = d.pop("typicalIntervalDays")

        days_since_last_purchase = d.pop("daysSinceLastPurchase")

        confidence = BuyReminderRowDtoConfidence(d.pop("confidence"))

        last_purchase = BuyReminderLastPurchaseDto.from_dict(d.pop("lastPurchase"))

        buy_reminder_row_dto = cls(
            identity_key=identity_key,
            display_name=display_name,
            brand=brand,
            barcode=barcode,
            last_purchase_at=last_purchase_at,
            typical_interval_days=typical_interval_days,
            days_since_last_purchase=days_since_last_purchase,
            confidence=confidence,
            last_purchase=last_purchase,
        )

        buy_reminder_row_dto.additional_properties = d
        return buy_reminder_row_dto

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
