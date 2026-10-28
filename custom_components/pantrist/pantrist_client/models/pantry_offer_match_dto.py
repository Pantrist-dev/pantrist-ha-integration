from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.offer_dto import OfferDto


T = TypeVar("T", bound="PantryOfferMatchDto")


@_attrs_define
class PantryOfferMatchDto:
    """
    Attributes:
        list_item_uuid (str): The pantry item's own uuid (list_item.uuid).
        article_name (str): The pantry item's own name, not the catalog ingredient's.
        amount (float):
        minimum_amount (float):
        store_id (str):
        store_name (str):
        retailer_key (str):
        offer (OfferDto):
    """

    list_item_uuid: str
    article_name: str
    amount: float
    minimum_amount: float
    store_id: str
    store_name: str
    retailer_key: str
    offer: OfferDto
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        list_item_uuid = self.list_item_uuid

        article_name = self.article_name

        amount = self.amount

        minimum_amount = self.minimum_amount

        store_id = self.store_id

        store_name = self.store_name

        retailer_key = self.retailer_key

        offer = self.offer.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "listItemUuid": list_item_uuid,
                "articleName": article_name,
                "amount": amount,
                "minimumAmount": minimum_amount,
                "storeId": store_id,
                "storeName": store_name,
                "retailerKey": retailer_key,
                "offer": offer,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offer_dto import OfferDto  # noqa: PLC0415

        d = dict(src_dict)
        list_item_uuid = d.pop("listItemUuid")

        article_name = d.pop("articleName")

        amount = d.pop("amount")

        minimum_amount = d.pop("minimumAmount")

        store_id = d.pop("storeId")

        store_name = d.pop("storeName")

        retailer_key = d.pop("retailerKey")

        offer = OfferDto.from_dict(d.pop("offer"))

        pantry_offer_match_dto = cls(
            list_item_uuid=list_item_uuid,
            article_name=article_name,
            amount=amount,
            minimum_amount=minimum_amount,
            store_id=store_id,
            store_name=store_name,
            retailer_key=retailer_key,
            offer=offer,
        )

        pantry_offer_match_dto.additional_properties = d
        return pantry_offer_match_dto

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
