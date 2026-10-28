from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RecipeMatchStateRequestDto")


@_attrs_define
class RecipeMatchStateRequestDto:
    """
    Attributes:
        uuids (list[str]): Recipe UUIDs to score against the authenticated user pantry Example: ['7c1bd6e3-…',
            'b48a01ff-…'].
        list_ids (list[str] | Unset): Scope the pantry the recipes are scored against to a subset of the user's lists.
            Used together with the `listIds` field on `ApiFilterDto` so the match badges on the home page line up with the
            same list the filter is using. Ids the caller does not own are silently dropped.
        ingredients (list[str] | Unset): Pantry item names to score against, for callers with no account. A signed-in
            caller leaves this unset and the server hydrates their pantry from their own lists, which is authoritative and
            cheaper. A local-only user has no lists to hydrate from, so the app ships the names it holds on the device
            instead. Same precedence as on `ApiFilterDto`: an explicit array wins, and the server-side hydration is skipped.
            Staples are matched from the recipe side (`recipe_ingredient.is_staple`) either way, so they do not need to be
            listed here.
    """

    uuids: list[str]
    list_ids: list[str] | Unset = UNSET
    ingredients: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuids = self.uuids

        list_ids: list[str] | Unset = UNSET
        if not isinstance(self.list_ids, Unset):
            list_ids = self.list_ids

        ingredients: list[str] | Unset = UNSET
        if not isinstance(self.ingredients, Unset):
            ingredients = self.ingredients

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuids": uuids,
            }
        )
        if list_ids is not UNSET:
            field_dict["listIds"] = list_ids
        if ingredients is not UNSET:
            field_dict["ingredients"] = ingredients

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuids = cast(list[str], d.pop("uuids"))

        list_ids = cast(list[str], d.pop("listIds", UNSET))

        ingredients = cast(list[str], d.pop("ingredients", UNSET))

        recipe_match_state_request_dto = cls(
            uuids=uuids,
            list_ids=list_ids,
            ingredients=ingredients,
        )

        recipe_match_state_request_dto.additional_properties = d
        return recipe_match_state_request_dto

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
