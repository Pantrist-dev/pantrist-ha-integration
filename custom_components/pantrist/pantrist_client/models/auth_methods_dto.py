from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.auth_methods_dto_providers_item import AuthMethodsDtoProvidersItem

T = TypeVar("T", bound="AuthMethodsDto")


@_attrs_define
class AuthMethodsDto:
    """
    Attributes:
        email (str):
        email_verified (bool):
        has_password (bool): Whether an email/password credential exists.
        providers (list[AuthMethodsDtoProvidersItem]):
    """

    email: str
    email_verified: bool
    has_password: bool
    providers: list[AuthMethodsDtoProvidersItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        email_verified = self.email_verified

        has_password = self.has_password

        providers = []
        for providers_item_data in self.providers:
            providers_item = providers_item_data.value
            providers.append(providers_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "emailVerified": email_verified,
                "hasPassword": has_password,
                "providers": providers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        email_verified = d.pop("emailVerified")

        has_password = d.pop("hasPassword")

        providers = []
        _providers = d.pop("providers")
        for providers_item_data in _providers:
            providers_item = AuthMethodsDtoProvidersItem(providers_item_data)

            providers.append(providers_item)

        auth_methods_dto = cls(
            email=email,
            email_verified=email_verified,
            has_password=has_password,
            providers=providers,
        )

        auth_methods_dto.additional_properties = d
        return auth_methods_dto

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
