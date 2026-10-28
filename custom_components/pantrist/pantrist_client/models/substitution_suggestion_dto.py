from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.substitution_suggestion_dto_confidence import SubstitutionSuggestionDtoConfidence
from ..models.substitution_suggestion_dto_kind import SubstitutionSuggestionDtoKind
from ..types import UNSET, Unset

T = TypeVar("T", bound="SubstitutionSuggestionDto")


@_attrs_define
class SubstitutionSuggestionDto:
    """
    Attributes:
        ingredient (str): The recipe ingredient name that is missing but substitutable Example: Butter.
        substitute_with (str): The pantry ingredient the user can use instead (localised display name) Example:
            Margarine.
        confidence (SubstitutionSuggestionDtoConfidence): How well the substitute stands in for the original Example:
            good.
        note (str | Unset): Optional hint for the swap, e.g. "use 80% of the amount"
        kind (SubstitutionSuggestionDtoKind | Unset): Why the pantry item can stand in: `variant` — the pantry holds a
            more generic kind of the requested ingredient (Tomaten for Kirschtomaten); `substitute` — a curated substitution
            edge.
    """

    ingredient: str
    substitute_with: str
    confidence: SubstitutionSuggestionDtoConfidence
    note: str | Unset = UNSET
    kind: SubstitutionSuggestionDtoKind | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        ingredient = self.ingredient

        substitute_with = self.substitute_with

        confidence = self.confidence.value

        note = self.note

        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ingredient": ingredient,
                "substituteWith": substitute_with,
                "confidence": confidence,
            }
        )
        if note is not UNSET:
            field_dict["note"] = note
        if kind is not UNSET:
            field_dict["kind"] = kind

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        ingredient = d.pop("ingredient")

        substitute_with = d.pop("substituteWith")

        confidence = SubstitutionSuggestionDtoConfidence(d.pop("confidence"))

        note = d.pop("note", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: SubstitutionSuggestionDtoKind | Unset
        if isinstance(_kind, Unset) or _kind is None or _kind == "":
            kind = UNSET
        else:
            kind = SubstitutionSuggestionDtoKind(_kind)

        substitution_suggestion_dto = cls(
            ingredient=ingredient,
            substitute_with=substitute_with,
            confidence=confidence,
            note=note,
            kind=kind,
        )

        substitution_suggestion_dto.additional_properties = d
        return substitution_suggestion_dto

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
