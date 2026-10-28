from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.provider_profile_dto import ProviderProfileDto


T = TypeVar("T", bound="ProviderLoginDto")


@_attrs_define
class ProviderLoginDto:
    """
    Attributes:
        client (str | Unset): Client label: ios, android, web, wear, …
        device_name (str | Unset): Human readable device name for the session list.
        id_token (str | Unset): Google / Apple ID token (JWT). Required for google.com and apple.com.
        access_token (str | Unset): Facebook access token. Required for facebook.com.
        nonce (str | Unset): Raw nonce sent to Apple, if the client used one.
        profile (ProviderProfileDto | Unset):
        language (str | Unset):
    """

    client: str | Unset = UNSET
    device_name: str | Unset = UNSET
    id_token: str | Unset = UNSET
    access_token: str | Unset = UNSET
    nonce: str | Unset = UNSET
    profile: ProviderProfileDto | Unset = UNSET
    language: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        client = self.client

        device_name = self.device_name

        id_token = self.id_token

        access_token = self.access_token

        nonce = self.nonce

        profile: dict[str, Any] | Unset = UNSET
        if not isinstance(self.profile, Unset):
            profile = self.profile.to_dict()

        language = self.language

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if client is not UNSET:
            field_dict["client"] = client
        if device_name is not UNSET:
            field_dict["deviceName"] = device_name
        if id_token is not UNSET:
            field_dict["idToken"] = id_token
        if access_token is not UNSET:
            field_dict["accessToken"] = access_token
        if nonce is not UNSET:
            field_dict["nonce"] = nonce
        if profile is not UNSET:
            field_dict["profile"] = profile
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.provider_profile_dto import ProviderProfileDto  # noqa: PLC0415

        d = dict(src_dict)
        client = d.pop("client", UNSET)

        device_name = d.pop("deviceName", UNSET)

        id_token = d.pop("idToken", UNSET)

        access_token = d.pop("accessToken", UNSET)

        nonce = d.pop("nonce", UNSET)

        _profile = d.pop("profile", UNSET)
        profile: ProviderProfileDto | Unset
        if isinstance(_profile, Unset) or _profile is None:
            profile = UNSET
        else:
            profile = ProviderProfileDto.from_dict(_profile)

        language = d.pop("language", UNSET)

        provider_login_dto = cls(
            client=client,
            device_name=device_name,
            id_token=id_token,
            access_token=access_token,
            nonce=nonce,
            profile=profile,
            language=language,
        )

        provider_login_dto.additional_properties = d
        return provider_login_dto

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
