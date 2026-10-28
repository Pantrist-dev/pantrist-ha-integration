from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.loyalty_card_format import LoyaltyCardFormat
from ..types import UNSET, Unset

T = TypeVar("T", bound="UpsertLoyaltyCardDto")


@_attrs_define
class UpsertLoyaltyCardDto:
    """
    Attributes:
        label (str): Display name, e.g. the market name.
        code (str): Card number or QR payload, exactly as encoded in the code.
        format_ (LoyaltyCardFormat):
        color (None | str | Unset): Card colour as #rrggbb, null for the default.
        retailer_key (None | str | Unset): Chain the card belongs to (e.g. "lidl"). Matches every market of that chain
            in every list. Set either this or listId + supermarketUid.
        list_id (None | str | Unset): List of the custom market the card belongs to.
        supermarket_uid (None | str | Unset): Uid of the custom market (in listId) the card belongs to.
        shared_list_id (None | str | Unset): List whose members may show the card too. Null keeps it private. Must equal
            listId for a card bound to a custom market.
    """

    label: str
    code: str
    format_: LoyaltyCardFormat
    color: None | str | Unset = UNSET
    retailer_key: None | str | Unset = UNSET
    list_id: None | str | Unset = UNSET
    supermarket_uid: None | str | Unset = UNSET
    shared_list_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        label = self.label

        code = self.code

        format_ = self.format_.value

        color: None | str | Unset
        if isinstance(self.color, Unset):
            color = UNSET
        else:
            color = self.color

        retailer_key: None | str | Unset
        if isinstance(self.retailer_key, Unset):
            retailer_key = UNSET
        else:
            retailer_key = self.retailer_key

        list_id: None | str | Unset
        if isinstance(self.list_id, Unset):
            list_id = UNSET
        else:
            list_id = self.list_id

        supermarket_uid: None | str | Unset
        if isinstance(self.supermarket_uid, Unset):
            supermarket_uid = UNSET
        else:
            supermarket_uid = self.supermarket_uid

        shared_list_id: None | str | Unset
        if isinstance(self.shared_list_id, Unset):
            shared_list_id = UNSET
        else:
            shared_list_id = self.shared_list_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "label": label,
                "code": code,
                "format": format_,
            }
        )
        if color is not UNSET:
            field_dict["color"] = color
        if retailer_key is not UNSET:
            field_dict["retailerKey"] = retailer_key
        if list_id is not UNSET:
            field_dict["listId"] = list_id
        if supermarket_uid is not UNSET:
            field_dict["supermarketUid"] = supermarket_uid
        if shared_list_id is not UNSET:
            field_dict["sharedListId"] = shared_list_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        label = d.pop("label")

        code = d.pop("code")

        format_ = LoyaltyCardFormat(d.pop("format"))

        def _parse_color(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        color = _parse_color(d.pop("color", UNSET))

        def _parse_retailer_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        retailer_key = _parse_retailer_key(d.pop("retailerKey", UNSET))

        def _parse_list_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        list_id = _parse_list_id(d.pop("listId", UNSET))

        def _parse_supermarket_uid(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        supermarket_uid = _parse_supermarket_uid(d.pop("supermarketUid", UNSET))

        def _parse_shared_list_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        shared_list_id = _parse_shared_list_id(d.pop("sharedListId", UNSET))

        upsert_loyalty_card_dto = cls(
            label=label,
            code=code,
            format_=format_,
            color=color,
            retailer_key=retailer_key,
            list_id=list_id,
            supermarket_uid=supermarket_uid,
            shared_list_id=shared_list_id,
        )

        upsert_loyalty_card_dto.additional_properties = d
        return upsert_loyalty_card_dto

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
