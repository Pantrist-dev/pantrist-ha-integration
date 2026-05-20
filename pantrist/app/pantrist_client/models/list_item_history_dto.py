from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.history_event_type import HistoryEventType
from ..models.history_item_type import HistoryItemType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_dto import ArticleDto
    from ..models.public_user_dto import PublicUserDto


T = TypeVar("T", bound="ListItemHistoryDto")


@_attrs_define
class ListItemHistoryDto:
    """
    Attributes:
        id (str):
        list_id (str):
        item_uuid (str):
        item_type (HistoryItemType):
        event_type (HistoryEventType):
        occurred_at (str): ISO timestamp when the change occurred
        changed_fields (list[str]): Names of the ArticleDto fields whose value changed. Empty for created/deleted.
        actor_uid (None | str | Unset):
        actor (PublicUserDto | Unset):
        before (ArticleDto | Unset):
        after (ArticleDto | Unset):
        reverted_from_id (None | str | Unset): Set if this entry was produced by reverting another history entry —
            points to that entry id.
    """

    id: str
    list_id: str
    item_uuid: str
    item_type: HistoryItemType
    event_type: HistoryEventType
    occurred_at: str
    changed_fields: list[str]
    actor_uid: None | str | Unset = UNSET
    actor: PublicUserDto | Unset = UNSET
    before: ArticleDto | Unset = UNSET
    after: ArticleDto | Unset = UNSET
    reverted_from_id: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        list_id = self.list_id

        item_uuid = self.item_uuid

        item_type = self.item_type.value

        event_type = self.event_type.value

        occurred_at = self.occurred_at

        changed_fields = self.changed_fields

        actor_uid: None | str | Unset
        if isinstance(self.actor_uid, Unset):
            actor_uid = UNSET
        else:
            actor_uid = self.actor_uid

        actor: dict[str, Any] | Unset = UNSET
        if not isinstance(self.actor, Unset):
            actor = self.actor.to_dict()

        before: dict[str, Any] | Unset = UNSET
        if not isinstance(self.before, Unset):
            before = self.before.to_dict()

        after: dict[str, Any] | Unset = UNSET
        if not isinstance(self.after, Unset):
            after = self.after.to_dict()

        reverted_from_id: None | str | Unset
        if isinstance(self.reverted_from_id, Unset):
            reverted_from_id = UNSET
        else:
            reverted_from_id = self.reverted_from_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "listId": list_id,
                "itemUuid": item_uuid,
                "itemType": item_type,
                "eventType": event_type,
                "occurredAt": occurred_at,
                "changedFields": changed_fields,
            }
        )
        if actor_uid is not UNSET:
            field_dict["actorUid"] = actor_uid
        if actor is not UNSET:
            field_dict["actor"] = actor
        if before is not UNSET:
            field_dict["before"] = before
        if after is not UNSET:
            field_dict["after"] = after
        if reverted_from_id is not UNSET:
            field_dict["revertedFromId"] = reverted_from_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_dto import ArticleDto
        from ..models.public_user_dto import PublicUserDto

        d = dict(src_dict)
        id = d.pop("id")

        list_id = d.pop("listId")

        item_uuid = d.pop("itemUuid")

        item_type = HistoryItemType(d.pop("itemType"))

        event_type = HistoryEventType(d.pop("eventType"))

        occurred_at = d.pop("occurredAt")

        changed_fields = cast(list[str], d.pop("changedFields"))

        def _parse_actor_uid(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        actor_uid = _parse_actor_uid(d.pop("actorUid", UNSET))

        _actor = d.pop("actor", UNSET)
        actor: PublicUserDto | Unset
        if isinstance(_actor, Unset):
            actor = UNSET
        else:
            actor = PublicUserDto.from_dict(_actor)

        _before = d.pop("before", UNSET)
        before: ArticleDto | Unset
        if isinstance(_before, Unset):
            before = UNSET
        else:
            before = ArticleDto.from_dict(_before)

        _after = d.pop("after", UNSET)
        after: ArticleDto | Unset
        if isinstance(_after, Unset):
            after = UNSET
        else:
            after = ArticleDto.from_dict(_after)

        def _parse_reverted_from_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        reverted_from_id = _parse_reverted_from_id(d.pop("revertedFromId", UNSET))

        list_item_history_dto = cls(
            id=id,
            list_id=list_id,
            item_uuid=item_uuid,
            item_type=item_type,
            event_type=event_type,
            occurred_at=occurred_at,
            changed_fields=changed_fields,
            actor_uid=actor_uid,
            actor=actor,
            before=before,
            after=after,
            reverted_from_id=reverted_from_id,
        )

        list_item_history_dto.additional_properties = d
        return list_item_history_dto

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
