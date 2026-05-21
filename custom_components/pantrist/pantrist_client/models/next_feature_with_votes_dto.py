from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.localization_dto import LocalizationDto


T = TypeVar("T", bound="NextFeatureWithVotesDto")


@_attrs_define
class NextFeatureWithVotesDto:
    """
    Attributes:
        id (str):
        name (LocalizationDto):
        votes (float):
    """

    id: str
    name: LocalizationDto
    votes: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name.to_dict()

        votes = self.votes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "name": name,
                "votes": votes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.localization_dto import LocalizationDto

        d = dict(src_dict)
        id = d.pop("id")

        name = LocalizationDto.from_dict(d.pop("name"))

        votes = d.pop("votes")

        next_feature_with_votes_dto = cls(
            id=id,
            name=name,
            votes=votes,
        )

        next_feature_with_votes_dto.additional_properties = d
        return next_feature_with_votes_dto

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
