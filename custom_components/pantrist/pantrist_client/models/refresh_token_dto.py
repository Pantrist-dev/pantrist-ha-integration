from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RefreshTokenDto")


@_attrs_define
class RefreshTokenDto:
    """
    Attributes:
        refresh_token (str | Unset): The refresh token. Optional only so a browser can present the HttpOnly refresh
            cookie instead, which is how a web app whose storage the browser cleared gets back in. One of the two must be
            there, and the body wins when both are.
        request_id (str | Unset): Opaque id identifying this renewal attempt. Generate one per renewal, keep it for
            every retry of that renewal including across app restarts, and drop it once the renewal succeeds. It lets the
            API tell a client retrying a request whose response was lost from someone replaying a stolen token, and serve
            the first without a time limit. Optional: without it the API falls back to a short grace window.
    """

    refresh_token: str | Unset = UNSET
    request_id: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        refresh_token = self.refresh_token

        request_id = self.request_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if refresh_token is not UNSET:
            field_dict["refreshToken"] = refresh_token
        if request_id is not UNSET:
            field_dict["requestId"] = request_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        refresh_token = d.pop("refreshToken", UNSET)

        request_id = d.pop("requestId", UNSET)

        refresh_token_dto = cls(
            refresh_token=refresh_token,
            request_id=request_id,
        )

        refresh_token_dto.additional_properties = d
        return refresh_token_dto

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
