from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RegisterDto")


@_attrs_define
class RegisterDto:
    """
    Attributes:
        email (str):
        password (str):
        display_name (str):
        client (str | Unset): Client label: ios, android, web, wear, …
        device_name (str | Unset): Human readable device name for the session list.
        language (str | Unset): BCP 47 language tag the app runs in.
    """

    email: str
    password: str
    display_name: str
    client: str | Unset = UNSET
    device_name: str | Unset = UNSET
    language: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        password = self.password

        display_name = self.display_name

        client = self.client

        device_name = self.device_name

        language = self.language

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "password": password,
                "displayName": display_name,
            }
        )
        if client is not UNSET:
            field_dict["client"] = client
        if device_name is not UNSET:
            field_dict["deviceName"] = device_name
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        email = d.pop("email")

        password = d.pop("password")

        display_name = d.pop("displayName")

        client = d.pop("client", UNSET)

        device_name = d.pop("deviceName", UNSET)

        language = d.pop("language", UNSET)

        register_dto = cls(
            email=email,
            password=password,
            display_name=display_name,
            client=client,
            device_name=device_name,
            language=language,
        )

        register_dto.additional_properties = d
        return register_dto

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
