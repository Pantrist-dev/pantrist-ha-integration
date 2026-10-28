from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_subscription_dto_status import UserSubscriptionDtoStatus
from ..models.user_subscription_dto_store import UserSubscriptionDtoStore
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserSubscriptionDto")


@_attrs_define
class UserSubscriptionDto:
    """
    Attributes:
        status (UserSubscriptionDtoStatus):
        expires_at (str):
        product_id (None | str | Unset):
        store (UserSubscriptionDtoStore | Unset):
        granted_manually (bool | Unset): Granted on the admin page rather than bought. Store events do not end it.
    """

    status: UserSubscriptionDtoStatus
    expires_at: str
    product_id: None | str | Unset = UNSET
    store: UserSubscriptionDtoStore | Unset = UNSET
    granted_manually: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        expires_at = self.expires_at

        product_id: None | str | Unset
        if isinstance(self.product_id, Unset):
            product_id = UNSET
        else:
            product_id = self.product_id

        store: str | Unset = UNSET
        if not isinstance(self.store, Unset):
            store = self.store.value

        granted_manually = self.granted_manually

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "expiresAt": expires_at,
            }
        )
        if product_id is not UNSET:
            field_dict["productId"] = product_id
        if store is not UNSET:
            field_dict["store"] = store
        if granted_manually is not UNSET:
            field_dict["grantedManually"] = granted_manually

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = UserSubscriptionDtoStatus(d.pop("status"))

        expires_at = d.pop("expiresAt")

        def _parse_product_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        product_id = _parse_product_id(d.pop("productId", UNSET))

        _store = d.pop("store", UNSET)
        store: UserSubscriptionDtoStore | Unset
        if isinstance(_store, Unset) or _store is None or _store == "":
            store = UNSET
        else:
            store = UserSubscriptionDtoStore(_store)

        granted_manually = d.pop("grantedManually", UNSET)

        user_subscription_dto = cls(
            status=status,
            expires_at=expires_at,
            product_id=product_id,
            store=store,
            granted_manually=granted_manually,
        )

        user_subscription_dto.additional_properties = d
        return user_subscription_dto

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
