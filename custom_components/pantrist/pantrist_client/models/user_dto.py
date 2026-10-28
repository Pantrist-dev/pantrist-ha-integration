from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_dto_forced_premium_tariff import UserDtoForcedPremiumTariff
from ..models.user_dto_user_country_source import UserDtoUserCountrySource
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.notification_settings_dto import NotificationSettingsDto
    from ..models.premium_invitation_data_dto import PremiumInvitationDataDto
    from ..models.user_permissions_dto import UserPermissionsDto
    from ..models.user_subscription_dto import UserSubscriptionDto


T = TypeVar("T", bound="UserDto")


@_attrs_define
class UserDto:
    """
    Attributes:
        uid (str):
        display_name (str):
        email (str):
        profile_image (str | Unset): Public profile picture key/URL. Safe to expose so members of a shared list can
            render each other’s avatars.
        forced_premium_tariff (UserDtoForcedPremiumTariff | Unset):
        language (str | Unset):
        email_verified (bool | Unset): Whether the email address has been confirmed (verification link, or inherited
            from the Firebase account on import).
        is_test_user (bool | Unset):
        provider_id (str | Unset):
        provider_uuid (str | Unset):
        subscription (UserSubscriptionDto | Unset):
        stripe_customer_id (str | Unset):
        stripe_subscription_id (str | Unset):
        current_list (str | Unset):
        permissions (UserPermissionsDto | Unset):
        user_country (str | Unset):
        user_country_source (UserDtoUserCountrySource | Unset):
        premium_invitation (PremiumInvitationDataDto | Unset):
        notification_settings (NotificationSettingsDto | Unset):
        last_seen (str | Unset): ISO timestamp of the last `/me/last-seen` ping. Used by analytics to track user
            activity (NOT the auto-reduce cursor — see `autoReduceCursor`).
        auto_reduce_cursor (str | Unset): ISO timestamp the app uses as the `since` parameter for the cold-start auto-
            reduce modal. Bumped via PATCH /me/auto-reduce-cursor after each modal presentation so accrual accumulates
            across sessions and stays in sync across devices.
        seen_tips (list[str] | Unset): The one-time tips (coach marks) this person has seen, on any device. Added via
            PUT /me/seen-tips/:tip.
    """

    uid: str
    display_name: str
    email: str
    profile_image: str | Unset = UNSET
    forced_premium_tariff: UserDtoForcedPremiumTariff | Unset = UNSET
    language: str | Unset = UNSET
    email_verified: bool | Unset = UNSET
    is_test_user: bool | Unset = UNSET
    provider_id: str | Unset = UNSET
    provider_uuid: str | Unset = UNSET
    subscription: UserSubscriptionDto | Unset = UNSET
    stripe_customer_id: str | Unset = UNSET
    stripe_subscription_id: str | Unset = UNSET
    current_list: str | Unset = UNSET
    permissions: UserPermissionsDto | Unset = UNSET
    user_country: str | Unset = UNSET
    user_country_source: UserDtoUserCountrySource | Unset = UNSET
    premium_invitation: PremiumInvitationDataDto | Unset = UNSET
    notification_settings: NotificationSettingsDto | Unset = UNSET
    last_seen: str | Unset = UNSET
    auto_reduce_cursor: str | Unset = UNSET
    seen_tips: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uid = self.uid

        display_name = self.display_name

        email = self.email

        profile_image = self.profile_image

        forced_premium_tariff: str | Unset = UNSET
        if not isinstance(self.forced_premium_tariff, Unset):
            forced_premium_tariff = self.forced_premium_tariff.value

        language = self.language

        email_verified = self.email_verified

        is_test_user = self.is_test_user

        provider_id = self.provider_id

        provider_uuid = self.provider_uuid

        subscription: dict[str, Any] | Unset = UNSET
        if not isinstance(self.subscription, Unset):
            subscription = self.subscription.to_dict()

        stripe_customer_id = self.stripe_customer_id

        stripe_subscription_id = self.stripe_subscription_id

        current_list = self.current_list

        permissions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.permissions, Unset):
            permissions = self.permissions.to_dict()

        user_country = self.user_country

        user_country_source: str | Unset = UNSET
        if not isinstance(self.user_country_source, Unset):
            user_country_source = self.user_country_source.value

        premium_invitation: dict[str, Any] | Unset = UNSET
        if not isinstance(self.premium_invitation, Unset):
            premium_invitation = self.premium_invitation.to_dict()

        notification_settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.notification_settings, Unset):
            notification_settings = self.notification_settings.to_dict()

        last_seen = self.last_seen

        auto_reduce_cursor = self.auto_reduce_cursor

        seen_tips: list[str] | Unset = UNSET
        if not isinstance(self.seen_tips, Unset):
            seen_tips = self.seen_tips

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uid": uid,
                "displayName": display_name,
                "email": email,
            }
        )
        if profile_image is not UNSET:
            field_dict["profileImage"] = profile_image
        if forced_premium_tariff is not UNSET:
            field_dict["forcedPremiumTariff"] = forced_premium_tariff
        if language is not UNSET:
            field_dict["language"] = language
        if email_verified is not UNSET:
            field_dict["emailVerified"] = email_verified
        if is_test_user is not UNSET:
            field_dict["isTestUser"] = is_test_user
        if provider_id is not UNSET:
            field_dict["providerId"] = provider_id
        if provider_uuid is not UNSET:
            field_dict["providerUuid"] = provider_uuid
        if subscription is not UNSET:
            field_dict["subscription"] = subscription
        if stripe_customer_id is not UNSET:
            field_dict["stripe_customer_id"] = stripe_customer_id
        if stripe_subscription_id is not UNSET:
            field_dict["stripe_subscription_id"] = stripe_subscription_id
        if current_list is not UNSET:
            field_dict["currentList"] = current_list
        if permissions is not UNSET:
            field_dict["permissions"] = permissions
        if user_country is not UNSET:
            field_dict["userCountry"] = user_country
        if user_country_source is not UNSET:
            field_dict["userCountrySource"] = user_country_source
        if premium_invitation is not UNSET:
            field_dict["premiumInvitation"] = premium_invitation
        if notification_settings is not UNSET:
            field_dict["notificationSettings"] = notification_settings
        if last_seen is not UNSET:
            field_dict["lastSeen"] = last_seen
        if auto_reduce_cursor is not UNSET:
            field_dict["autoReduceCursor"] = auto_reduce_cursor
        if seen_tips is not UNSET:
            field_dict["seenTips"] = seen_tips

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.notification_settings_dto import NotificationSettingsDto  # noqa: PLC0415
        from ..models.premium_invitation_data_dto import PremiumInvitationDataDto  # noqa: PLC0415
        from ..models.user_permissions_dto import UserPermissionsDto  # noqa: PLC0415
        from ..models.user_subscription_dto import UserSubscriptionDto  # noqa: PLC0415

        d = dict(src_dict)
        uid = d.pop("uid")

        display_name = d.pop("displayName")

        email = d.pop("email")

        profile_image = d.pop("profileImage", UNSET)

        _forced_premium_tariff = d.pop("forcedPremiumTariff", UNSET)
        forced_premium_tariff: UserDtoForcedPremiumTariff | Unset
        if isinstance(_forced_premium_tariff, Unset) or _forced_premium_tariff is None or _forced_premium_tariff == "":
            forced_premium_tariff = UNSET
        else:
            forced_premium_tariff = UserDtoForcedPremiumTariff(_forced_premium_tariff)

        language = d.pop("language", UNSET)

        email_verified = d.pop("emailVerified", UNSET)

        is_test_user = d.pop("isTestUser", UNSET)

        provider_id = d.pop("providerId", UNSET)

        provider_uuid = d.pop("providerUuid", UNSET)

        _subscription = d.pop("subscription", UNSET)
        subscription: UserSubscriptionDto | Unset
        if isinstance(_subscription, Unset) or _subscription is None:
            subscription = UNSET
        else:
            subscription = UserSubscriptionDto.from_dict(_subscription)

        stripe_customer_id = d.pop("stripe_customer_id", UNSET)

        stripe_subscription_id = d.pop("stripe_subscription_id", UNSET)

        current_list = d.pop("currentList", UNSET)

        _permissions = d.pop("permissions", UNSET)
        permissions: UserPermissionsDto | Unset
        if isinstance(_permissions, Unset) or _permissions is None:
            permissions = UNSET
        else:
            permissions = UserPermissionsDto.from_dict(_permissions)

        user_country = d.pop("userCountry", UNSET)

        _user_country_source = d.pop("userCountrySource", UNSET)
        user_country_source: UserDtoUserCountrySource | Unset
        if isinstance(_user_country_source, Unset) or _user_country_source is None or _user_country_source == "":
            user_country_source = UNSET
        else:
            user_country_source = UserDtoUserCountrySource(_user_country_source)

        _premium_invitation = d.pop("premiumInvitation", UNSET)
        premium_invitation: PremiumInvitationDataDto | Unset
        if isinstance(_premium_invitation, Unset) or _premium_invitation is None:
            premium_invitation = UNSET
        else:
            premium_invitation = PremiumInvitationDataDto.from_dict(_premium_invitation)

        _notification_settings = d.pop("notificationSettings", UNSET)
        notification_settings: NotificationSettingsDto | Unset
        if isinstance(_notification_settings, Unset) or _notification_settings is None:
            notification_settings = UNSET
        else:
            notification_settings = NotificationSettingsDto.from_dict(_notification_settings)

        last_seen = d.pop("lastSeen", UNSET)

        auto_reduce_cursor = d.pop("autoReduceCursor", UNSET)

        seen_tips = cast(list[str], d.pop("seenTips", UNSET))

        user_dto = cls(
            uid=uid,
            display_name=display_name,
            email=email,
            profile_image=profile_image,
            forced_premium_tariff=forced_premium_tariff,
            language=language,
            email_verified=email_verified,
            is_test_user=is_test_user,
            provider_id=provider_id,
            provider_uuid=provider_uuid,
            subscription=subscription,
            stripe_customer_id=stripe_customer_id,
            stripe_subscription_id=stripe_subscription_id,
            current_list=current_list,
            permissions=permissions,
            user_country=user_country,
            user_country_source=user_country_source,
            premium_invitation=premium_invitation,
            notification_settings=notification_settings,
            last_seen=last_seen,
            auto_reduce_cursor=auto_reduce_cursor,
            seen_tips=seen_tips,
        )

        user_dto.additional_properties = d
        return user_dto

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
