from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_dto import UserDto


T = TypeVar("T", bound="AuthSessionResponseDto")


@_attrs_define
class AuthSessionResponseDto:
    """
    Attributes:
        access_token (str): JWT to send as `Authorization: Bearer …`.
        expires_in (float): Seconds until the access token expires.
        refresh_token (str): Opaque token for POST /auth/token/refresh. Rotates on every refresh; store the newest one
            and never refresh concurrently.
        token_type (str):  Example: Bearer.
        session_id (str): Id of the session the tokens belong to.
        is_new_user (bool): True when this call created the account.
        user (UserDto | Unset):
    """

    access_token: str
    expires_in: float
    refresh_token: str
    token_type: str
    session_id: str
    is_new_user: bool
    user: UserDto | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        access_token = self.access_token

        expires_in = self.expires_in

        refresh_token = self.refresh_token

        token_type = self.token_type

        session_id = self.session_id

        is_new_user = self.is_new_user

        user: dict[str, Any] | Unset = UNSET
        if not isinstance(self.user, Unset):
            user = self.user.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "accessToken": access_token,
                "expiresIn": expires_in,
                "refreshToken": refresh_token,
                "tokenType": token_type,
                "sessionId": session_id,
                "isNewUser": is_new_user,
            }
        )
        if user is not UNSET:
            field_dict["user"] = user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_dto import UserDto  # noqa: PLC0415

        d = dict(src_dict)
        access_token = d.pop("accessToken")

        expires_in = d.pop("expiresIn")

        refresh_token = d.pop("refreshToken")

        token_type = d.pop("tokenType")

        session_id = d.pop("sessionId")

        is_new_user = d.pop("isNewUser")

        _user = d.pop("user", UNSET)
        user: UserDto | Unset
        if isinstance(_user, Unset) or _user is None:
            user = UNSET
        else:
            user = UserDto.from_dict(_user)

        auth_session_response_dto = cls(
            access_token=access_token,
            expires_in=expires_in,
            refresh_token=refresh_token,
            token_type=token_type,
            session_id=session_id,
            is_new_user=is_new_user,
            user=user,
        )

        auth_session_response_dto.additional_properties = d
        return auth_session_response_dto

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
