from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.article_dto import ArticleDto


T = TypeVar("T", bound="ItemListDto")


@_attrs_define
class ItemListDto:
    """
    Attributes:
        list_id (str): ID of the list of the items
        items (list[ArticleDto]): Found items
    """

    list_id: str
    items: list[ArticleDto]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        list_id = self.list_id

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "listId": list_id,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_dto import ArticleDto

        d = dict(src_dict)
        list_id = d.pop("listId")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = ArticleDto.from_dict(items_item_data)

            items.append(items_item)

        item_list_dto = cls(
            list_id=list_id,
            items=items,
        )

        item_list_dto.additional_properties = d
        return item_list_dto

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
