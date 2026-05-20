from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.purchased_item_dto import PurchasedItemDto


T = TypeVar("T", bound="ListPurchasesControllerGetPurchasesResponse200")


@_attrs_define
class ListPurchasesControllerGetPurchasesResponse200:
    """
    Attributes:
        list_ (list[PurchasedItemDto] | Unset):
    """

    list_: list[PurchasedItemDto] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        list_: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.list_, Unset):
            list_ = []
            for list_item_data in self.list_:
                list_item = list_item_data.to_dict()
                list_.append(list_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if list_ is not UNSET:
            field_dict["list"] = list_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.purchased_item_dto import PurchasedItemDto

        d = dict(src_dict)
        _list_ = d.pop("list", UNSET)
        list_: list[PurchasedItemDto] | Unset = UNSET
        if _list_ is not UNSET:
            list_ = []
            for list_item_data in _list_:
                list_item = PurchasedItemDto.from_dict(list_item_data)

                list_.append(list_item)

        list_purchases_controller_get_purchases_response_200 = cls(
            list_=list_,
        )

        list_purchases_controller_get_purchases_response_200.additional_properties = d
        return list_purchases_controller_get_purchases_response_200

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
