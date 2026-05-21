from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="MessageDto")


@_attrs_define
class MessageDto:
    """
    Attributes:
        from_ (str):
        subject (str):
        message (str):
        language (str):
        send_no_response (bool):
        cloudflare_token (str):
    """

    from_: str
    subject: str
    message: str
    language: str
    send_no_response: bool
    cloudflare_token: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from_ = self.from_

        subject = self.subject

        message = self.message

        language = self.language

        send_no_response = self.send_no_response

        cloudflare_token = self.cloudflare_token

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "subject": subject,
                "message": message,
                "language": language,
                "sendNoResponse": send_no_response,
                "cloudflareToken": cloudflare_token,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        from_ = d.pop("from")

        subject = d.pop("subject")

        message = d.pop("message")

        language = d.pop("language")

        send_no_response = d.pop("sendNoResponse")

        cloudflare_token = d.pop("cloudflareToken")

        message_dto = cls(
            from_=from_,
            subject=subject,
            message=message,
            language=language,
            send_no_response=send_no_response,
            cloudflare_token=cloudflare_token,
        )

        message_dto.additional_properties = d
        return message_dto

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
