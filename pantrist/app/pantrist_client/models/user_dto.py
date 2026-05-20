from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.user_dto_forced_premium_tariff import UserDtoForcedPremiumTariff
from ..models.user_dto_user_country_source import UserDtoUserCountrySource
from ..types import UNSET, Unset

if TYPE_CHECKING:
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
        forced_premium_tariff (UserDtoForcedPremiumTariff | Unset):
        is_test_user (bool | Unset):
        profile_image (str | Unset):
        provider_id (str | Unset):
        provider_uuid (str | Unset):
        subscription (UserSubscriptionDto | Unset):
        stripe_customer_id (str | Unset):
        stripe_subscription_id (str | Unset):
        current_list (str | Unset):
        permissions (UserPermissionsDto | Unset):
        user_country (str | Unset):
        user_country_source (UserDtoUserCountrySource | Unset):
    """

    uid: str
    display_name: str
    email: str
    forced_premium_tariff: UserDtoForcedPremiumTariff | Unset = UNSET
    is_test_user: bool | Unset = UNSET
    profile_image: str | Unset = UNSET
    provider_id: str | Unset = UNSET
    provider_uuid: str | Unset = UNSET
    subscription: UserSubscriptionDto | Unset = UNSET
    stripe_customer_id: str | Unset = UNSET
    stripe_subscription_id: str | Unset = UNSET
    current_list: str | Unset = UNSET
    permissions: UserPermissionsDto | Unset = UNSET
    user_country: str | Unset = UNSET
    user_country_source: UserDtoUserCountrySource | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uid = self.uid

        display_name = self.display_name

        email = self.email

        forced_premium_tariff: str | Unset = UNSET
        if not isinstance(self.forced_premium_tariff, Unset):
            forced_premium_tariff = self.forced_premium_tariff.value

        is_test_user = self.is_test_user

        profile_image = self.profile_image

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

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uid": uid,
                "displayName": display_name,
                "email": email,
            }
        )
        if forced_premium_tariff is not UNSET:
            field_dict["forcedPremiumTariff"] = forced_premium_tariff
        if is_test_user is not UNSET:
            field_dict["isTestUser"] = is_test_user
        if profile_image is not UNSET:
            field_dict["profileImage"] = profile_image
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_permissions_dto import UserPermissionsDto
        from ..models.user_subscription_dto import UserSubscriptionDto

        d = dict(src_dict)
        uid = d.pop("uid")

        display_name = d.pop("displayName")

        email = d.pop("email")

        _forced_premium_tariff = d.pop("forcedPremiumTariff", UNSET)
        forced_premium_tariff: UserDtoForcedPremiumTariff | Unset
        if isinstance(_forced_premium_tariff, Unset):
            forced_premium_tariff = UNSET
        else:
            forced_premium_tariff = UserDtoForcedPremiumTariff(_forced_premium_tariff)

        is_test_user = d.pop("isTestUser", UNSET)

        profile_image = d.pop("profileImage", UNSET)

        provider_id = d.pop("providerId", UNSET)

        provider_uuid = d.pop("providerUuid", UNSET)

        _subscription = d.pop("subscription", UNSET)
        subscription: UserSubscriptionDto | Unset
        if isinstance(_subscription, Unset):
            subscription = UNSET
        else:
            subscription = UserSubscriptionDto.from_dict(_subscription)

        stripe_customer_id = d.pop("stripe_customer_id", UNSET)

        stripe_subscription_id = d.pop("stripe_subscription_id", UNSET)

        current_list = d.pop("currentList", UNSET)

        _permissions = d.pop("permissions", UNSET)
        permissions: UserPermissionsDto | Unset
        if isinstance(_permissions, Unset):
            permissions = UNSET
        else:
            permissions = UserPermissionsDto.from_dict(_permissions)

        user_country = d.pop("userCountry", UNSET)

        _user_country_source = d.pop("userCountrySource", UNSET)
        user_country_source: UserDtoUserCountrySource | Unset
        if isinstance(_user_country_source, Unset):
            user_country_source = UNSET
        else:
            user_country_source = UserDtoUserCountrySource(_user_country_source)

        user_dto = cls(
            uid=uid,
            display_name=display_name,
            email=email,
            forced_premium_tariff=forced_premium_tariff,
            is_test_user=is_test_user,
            profile_image=profile_image,
            provider_id=provider_id,
            provider_uuid=provider_uuid,
            subscription=subscription,
            stripe_customer_id=stripe_customer_id,
            stripe_subscription_id=stripe_subscription_id,
            current_list=current_list,
            permissions=permissions,
            user_country=user_country,
            user_country_source=user_country_source,
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
