from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_subscription_dto_status import UserSubscriptionDtoStatus

T = TypeVar("T", bound="UserSubscriptionDto")


@_attrs_define
class UserSubscriptionDto:
    """
    Attributes:
        status (UserSubscriptionDtoStatus):
        product_id (str):
        expires_at (str):
    """

    status: UserSubscriptionDtoStatus
    product_id: str
    expires_at: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        status = self.status.value

        product_id = self.product_id

        expires_at = self.expires_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "productId": product_id,
                "expiresAt": expires_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = UserSubscriptionDtoStatus(d.pop("status"))

        product_id = d.pop("productId")

        expires_at = d.pop("expiresAt")

        user_subscription_dto = cls(
            status=status,
            product_id=product_id,
            expires_at=expires_at,
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
