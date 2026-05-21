from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateBillingSessionDto")


@_attrs_define
class CreateBillingSessionDto:
    """
    Attributes:
        redirect_url (str):
        customer_id (str):
        stripe_customer_id (str):
    """

    redirect_url: str
    customer_id: str
    stripe_customer_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        redirect_url = self.redirect_url

        customer_id = self.customer_id

        stripe_customer_id = self.stripe_customer_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "redirectUrl": redirect_url,
                "customerId": customer_id,
                "stripeCustomerId": stripe_customer_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        redirect_url = d.pop("redirectUrl")

        customer_id = d.pop("customerId")

        stripe_customer_id = d.pop("stripeCustomerId")

        create_billing_session_dto = cls(
            redirect_url=redirect_url,
            customer_id=customer_id,
            stripe_customer_id=stripe_customer_id,
        )

        create_billing_session_dto.additional_properties = d
        return create_billing_session_dto

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
