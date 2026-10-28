from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ai_role import AiRole
from ..models.recipe_origin import RecipeOrigin
from ..models.social_platform import SocialPlatform
from ..types import UNSET, Unset

T = TypeVar("T", bound="RecipeSourceDto")


@_attrs_define
class RecipeSourceDto:
    """
    Attributes:
        origin (RecipeOrigin):
        ai_role (AiRole):
        user_modified (bool): True once the user edited a recipe whose content a model produced. The AI badge stays
            either way, it only changes wording.
        platform (SocialPlatform | Unset): Set for social imports, drives the platform icon.
        channel_name (str | Unset): Channel or author handle, e.g. "@veganevibes".
        original_url (str | Unset): Link to the original post or page.
        site_name (str | Unset): Site name for web imports, e.g. "chefkoch.de".
        ai_generated_at (str | Unset): When the content was generated (ISO timestamp). Only set for aiRole=generated.
            Offer prices age, so the app shows this next to them.
    """

    origin: RecipeOrigin
    ai_role: AiRole
    user_modified: bool
    platform: SocialPlatform | Unset = UNSET
    channel_name: str | Unset = UNSET
    original_url: str | Unset = UNSET
    site_name: str | Unset = UNSET
    ai_generated_at: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        origin = self.origin.value

        ai_role = self.ai_role.value

        user_modified = self.user_modified

        platform: str | Unset = UNSET
        if not isinstance(self.platform, Unset):
            platform = self.platform.value

        channel_name = self.channel_name

        original_url = self.original_url

        site_name = self.site_name

        ai_generated_at = self.ai_generated_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "origin": origin,
                "aiRole": ai_role,
                "userModified": user_modified,
            }
        )
        if platform is not UNSET:
            field_dict["platform"] = platform
        if channel_name is not UNSET:
            field_dict["channelName"] = channel_name
        if original_url is not UNSET:
            field_dict["originalUrl"] = original_url
        if site_name is not UNSET:
            field_dict["siteName"] = site_name
        if ai_generated_at is not UNSET:
            field_dict["aiGeneratedAt"] = ai_generated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        origin = RecipeOrigin(d.pop("origin"))

        ai_role = AiRole(d.pop("aiRole"))

        user_modified = d.pop("userModified")

        _platform = d.pop("platform", UNSET)
        platform: SocialPlatform | Unset
        if isinstance(_platform, Unset) or _platform is None or _platform == "":
            platform = UNSET
        else:
            platform = SocialPlatform(_platform)

        channel_name = d.pop("channelName", UNSET)

        original_url = d.pop("originalUrl", UNSET)

        site_name = d.pop("siteName", UNSET)

        ai_generated_at = d.pop("aiGeneratedAt", UNSET)

        recipe_source_dto = cls(
            origin=origin,
            ai_role=ai_role,
            user_modified=user_modified,
            platform=platform,
            channel_name=channel_name,
            original_url=original_url,
            site_name=site_name,
            ai_generated_at=ai_generated_at,
        )

        recipe_source_dto.additional_properties = d
        return recipe_source_dto

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
