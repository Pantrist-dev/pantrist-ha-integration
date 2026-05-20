from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateUserDto")


@_attrs_define
class CreateUserDto:
    """
    Attributes:
        uid (str):
        email (str):
        display_name (str):
        profile_image (str | Unset):
        current_list (str | Unset):
        language (str | Unset):
    """

    uid: str
    email: str
    display_name: str
    profile_image: str | Unset = UNSET
    current_list: str | Unset = UNSET
    language: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uid = self.uid

        email = self.email

        display_name = self.display_name

        profile_image = self.profile_image

        current_list = self.current_list

        language = self.language

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uid": uid,
                "email": email,
                "displayName": display_name,
            }
        )
        if profile_image is not UNSET:
            field_dict["profileImage"] = profile_image
        if current_list is not UNSET:
            field_dict["currentList"] = current_list
        if language is not UNSET:
            field_dict["language"] = language

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uid = d.pop("uid")

        email = d.pop("email")

        display_name = d.pop("displayName")

        profile_image = d.pop("profileImage", UNSET)

        current_list = d.pop("currentList", UNSET)

        language = d.pop("language", UNSET)

        create_user_dto = cls(
            uid=uid,
            email=email,
            display_name=display_name,
            profile_image=profile_image,
            current_list=current_list,
            language=language,
        )

        create_user_dto.additional_properties = d
        return create_user_dto

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
