from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.block_settings_dto import BlockSettingsDto
    from ..models.list_user_dto import ListUserDto


T = TypeVar("T", bound="ListDto")


@_attrs_define
class ListDto:
    """
    Attributes:
        id (str): ID of the list
        name (str): Name of the list
        user_count (float): Count of users that have access to the list.
        shopping_item_count (float): Count of active shopping items in the list.
        current_list (bool): Whether the list is your current list.
        settings (BlockSettingsDto | Unset):
        users (list[ListUserDto] | Unset): Users with access to this list
    """

    id: str
    name: str
    user_count: float
    shopping_item_count: float
    current_list: bool
    settings: BlockSettingsDto | Unset = UNSET
    users: list[ListUserDto] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        user_count = self.user_count

        shopping_item_count = self.shopping_item_count

        current_list = self.current_list

        settings: dict[str, Any] | Unset = UNSET
        if not isinstance(self.settings, Unset):
            settings = self.settings.to_dict()

        users: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()
                users.append(users_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "userCount": user_count,
                "shoppingItemCount": shopping_item_count,
                "currentList": current_list,
            }
        )
        if settings is not UNSET:
            field_dict["settings"] = settings
        if users is not UNSET:
            field_dict["users"] = users

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.block_settings_dto import BlockSettingsDto
        from ..models.list_user_dto import ListUserDto

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        user_count = d.pop("userCount")

        shopping_item_count = d.pop("shoppingItemCount")

        current_list = d.pop("currentList")

        _settings = d.pop("settings", UNSET)
        settings: BlockSettingsDto | Unset
        if isinstance(_settings, Unset):
            settings = UNSET
        else:
            settings = BlockSettingsDto.from_dict(_settings)

        _users = d.pop("users", UNSET)
        users: list[ListUserDto] | Unset = UNSET
        if _users is not UNSET:
            users = []
            for users_item_data in _users:
                users_item = ListUserDto.from_dict(users_item_data)

                users.append(users_item)

        list_dto = cls(
            id=id,
            name=name,
            user_count=user_count,
            shopping_item_count=shopping_item_count,
            current_list=current_list,
            settings=settings,
            users=users,
        )

        list_dto.additional_properties = d
        return list_dto

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
