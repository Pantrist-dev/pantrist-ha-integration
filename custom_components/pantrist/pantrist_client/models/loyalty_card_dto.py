from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.loyalty_card_format import LoyaltyCardFormat

T = TypeVar("T", bound="LoyaltyCardDto")


@_attrs_define
class LoyaltyCardDto:
    """
    Attributes:
        uuid (str):
        owner_uid (str): The user who owns and may edit the card.
        label (str):
        code (str):
        format_ (LoyaltyCardFormat):
        color (None | str):
        retailer_key (None | str):
        list_id (None | str):
        supermarket_uid (None | str):
        shared_list_id (None | str): List the card is shared with. Null when private, and also when the owner has left
            that list.
        updated_at (datetime.datetime):
    """

    uuid: str
    owner_uid: str
    label: str
    code: str
    format_: LoyaltyCardFormat
    color: None | str
    retailer_key: None | str
    list_id: None | str
    supermarket_uid: None | str
    shared_list_id: None | str
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        owner_uid = self.owner_uid

        label = self.label

        code = self.code

        format_ = self.format_.value

        color: None | str
        color = self.color

        retailer_key: None | str
        retailer_key = self.retailer_key

        list_id: None | str
        list_id = self.list_id

        supermarket_uid: None | str
        supermarket_uid = self.supermarket_uid

        shared_list_id: None | str
        shared_list_id = self.shared_list_id

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "ownerUid": owner_uid,
                "label": label,
                "code": code,
                "format": format_,
                "color": color,
                "retailerKey": retailer_key,
                "listId": list_id,
                "supermarketUid": supermarket_uid,
                "sharedListId": shared_list_id,
                "updatedAt": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = d.pop("uuid")

        owner_uid = d.pop("ownerUid")

        label = d.pop("label")

        code = d.pop("code")

        format_ = LoyaltyCardFormat(d.pop("format"))

        def _parse_color(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        color = _parse_color(d.pop("color"))

        def _parse_retailer_key(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        retailer_key = _parse_retailer_key(d.pop("retailerKey"))

        def _parse_list_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        list_id = _parse_list_id(d.pop("listId"))

        def _parse_supermarket_uid(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        supermarket_uid = _parse_supermarket_uid(d.pop("supermarketUid"))

        def _parse_shared_list_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        shared_list_id = _parse_shared_list_id(d.pop("sharedListId"))

        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))

        loyalty_card_dto = cls(
            uuid=uuid,
            owner_uid=owner_uid,
            label=label,
            code=code,
            format_=format_,
            color=color,
            retailer_key=retailer_key,
            list_id=list_id,
            supermarket_uid=supermarket_uid,
            shared_list_id=shared_list_id,
            updated_at=updated_at,
        )

        loyalty_card_dto.additional_properties = d
        return loyalty_card_dto

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
