from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.app_version_policy_dto_platform import AppVersionPolicyDtoPlatform

T = TypeVar("T", bound="AppVersionPolicyDto")


@_attrs_define
class AppVersionPolicyDto:
    """
    Attributes:
        platform (AppVersionPolicyDtoPlatform):
        minimum_version (None | str): Versions below this are blocked until updated. Null when nothing is forced.
        recommended_version (None | str): Versions below this get a dismissible hint. Null when there is none.
        message_de (None | str): Why the update is needed, in German.
        message_en (None | str): Why the update is needed, in English.
    """

    platform: AppVersionPolicyDtoPlatform
    minimum_version: None | str
    recommended_version: None | str
    message_de: None | str
    message_en: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        platform = self.platform.value

        minimum_version: None | str
        minimum_version = self.minimum_version

        recommended_version: None | str
        recommended_version = self.recommended_version

        message_de: None | str
        message_de = self.message_de

        message_en: None | str
        message_en = self.message_en

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "platform": platform,
                "minimumVersion": minimum_version,
                "recommendedVersion": recommended_version,
                "messageDe": message_de,
                "messageEn": message_en,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        platform = AppVersionPolicyDtoPlatform(d.pop("platform"))

        def _parse_minimum_version(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        minimum_version = _parse_minimum_version(d.pop("minimumVersion"))

        def _parse_recommended_version(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        recommended_version = _parse_recommended_version(d.pop("recommendedVersion"))

        def _parse_message_de(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        message_de = _parse_message_de(d.pop("messageDe"))

        def _parse_message_en(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        message_en = _parse_message_en(d.pop("messageEn"))

        app_version_policy_dto = cls(
            platform=platform,
            minimum_version=minimum_version,
            recommended_version=recommended_version,
            message_de=message_de,
            message_en=message_en,
        )

        app_version_policy_dto.additional_properties = d
        return app_version_policy_dto

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
