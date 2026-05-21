from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.block_settings_dto import BlockSettingsDto
    from ..models.create_list_permission_dto import CreateListPermissionDto


T = TypeVar("T", bound="CreateListDto")


@_attrs_define
class CreateListDto:
    """
    Attributes:
        uuid (str): UUID for the new list
        settings (BlockSettingsDto):
        users (list[str]): Array of user UIDs with access
        permissions (list[CreateListPermissionDto]): Explicit permission entries (overrides users array)
    """

    uuid: str
    settings: BlockSettingsDto
    users: list[str]
    permissions: list[CreateListPermissionDto]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        settings = self.settings.to_dict()

        users = self.users

        permissions = []
        for permissions_item_data in self.permissions:
            permissions_item = permissions_item_data.to_dict()
            permissions.append(permissions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "settings": settings,
                "users": users,
                "permissions": permissions,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.block_settings_dto import BlockSettingsDto
        from ..models.create_list_permission_dto import CreateListPermissionDto

        d = dict(src_dict)
        uuid = d.pop("uuid")

        settings = BlockSettingsDto.from_dict(d.pop("settings"))

        users = cast(list[str], d.pop("users"))

        permissions = []
        _permissions = d.pop("permissions")
        for permissions_item_data in _permissions:
            permissions_item = CreateListPermissionDto.from_dict(permissions_item_data)

            permissions.append(permissions_item)

        create_list_dto = cls(
            uuid=uuid,
            settings=settings,
            users=users,
            permissions=permissions,
        )

        create_list_dto.additional_properties = d
        return create_list_dto

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
