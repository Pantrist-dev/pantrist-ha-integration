from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.nutri_score import NutriScore
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.general_nutriments_dto import GeneralNutrimentsDto


T = TypeVar("T", bound="ArticleNutrimentsDto")


@_attrs_define
class ArticleNutrimentsDto:
    """
    Attributes:
        energy_kcal (GeneralNutrimentsDto | Unset):
        energy_kj (GeneralNutrimentsDto | Unset):
        fat (GeneralNutrimentsDto | Unset):
        saturated_fat (GeneralNutrimentsDto | Unset):
        carbohydrates (GeneralNutrimentsDto | Unset):
        sugar (GeneralNutrimentsDto | Unset):
        fiber (GeneralNutrimentsDto | Unset):
        proteins (GeneralNutrimentsDto | Unset):
        salt (GeneralNutrimentsDto | Unset):
        nutri_score (NutriScore | Unset): Nutri-Score rating
    """

    energy_kcal: GeneralNutrimentsDto | Unset = UNSET
    energy_kj: GeneralNutrimentsDto | Unset = UNSET
    fat: GeneralNutrimentsDto | Unset = UNSET
    saturated_fat: GeneralNutrimentsDto | Unset = UNSET
    carbohydrates: GeneralNutrimentsDto | Unset = UNSET
    sugar: GeneralNutrimentsDto | Unset = UNSET
    fiber: GeneralNutrimentsDto | Unset = UNSET
    proteins: GeneralNutrimentsDto | Unset = UNSET
    salt: GeneralNutrimentsDto | Unset = UNSET
    nutri_score: NutriScore | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        energy_kcal: dict[str, Any] | Unset = UNSET
        if not isinstance(self.energy_kcal, Unset):
            energy_kcal = self.energy_kcal.to_dict()

        energy_kj: dict[str, Any] | Unset = UNSET
        if not isinstance(self.energy_kj, Unset):
            energy_kj = self.energy_kj.to_dict()

        fat: dict[str, Any] | Unset = UNSET
        if not isinstance(self.fat, Unset):
            fat = self.fat.to_dict()

        saturated_fat: dict[str, Any] | Unset = UNSET
        if not isinstance(self.saturated_fat, Unset):
            saturated_fat = self.saturated_fat.to_dict()

        carbohydrates: dict[str, Any] | Unset = UNSET
        if not isinstance(self.carbohydrates, Unset):
            carbohydrates = self.carbohydrates.to_dict()

        sugar: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sugar, Unset):
            sugar = self.sugar.to_dict()

        fiber: dict[str, Any] | Unset = UNSET
        if not isinstance(self.fiber, Unset):
            fiber = self.fiber.to_dict()

        proteins: dict[str, Any] | Unset = UNSET
        if not isinstance(self.proteins, Unset):
            proteins = self.proteins.to_dict()

        salt: dict[str, Any] | Unset = UNSET
        if not isinstance(self.salt, Unset):
            salt = self.salt.to_dict()

        nutri_score: str | Unset = UNSET
        if not isinstance(self.nutri_score, Unset):
            nutri_score = self.nutri_score.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if energy_kcal is not UNSET:
            field_dict["energy_kcal"] = energy_kcal
        if energy_kj is not UNSET:
            field_dict["energy_kj"] = energy_kj
        if fat is not UNSET:
            field_dict["fat"] = fat
        if saturated_fat is not UNSET:
            field_dict["saturatedFat"] = saturated_fat
        if carbohydrates is not UNSET:
            field_dict["carbohydrates"] = carbohydrates
        if sugar is not UNSET:
            field_dict["sugar"] = sugar
        if fiber is not UNSET:
            field_dict["fiber"] = fiber
        if proteins is not UNSET:
            field_dict["proteins"] = proteins
        if salt is not UNSET:
            field_dict["salt"] = salt
        if nutri_score is not UNSET:
            field_dict["nutriScore"] = nutri_score

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.general_nutriments_dto import GeneralNutrimentsDto

        d = dict(src_dict)
        _energy_kcal = d.pop("energy_kcal", UNSET)
        energy_kcal: GeneralNutrimentsDto | Unset
        if isinstance(_energy_kcal, Unset):
            energy_kcal = UNSET
        else:
            energy_kcal = GeneralNutrimentsDto.from_dict(_energy_kcal)

        _energy_kj = d.pop("energy_kj", UNSET)
        energy_kj: GeneralNutrimentsDto | Unset
        if isinstance(_energy_kj, Unset):
            energy_kj = UNSET
        else:
            energy_kj = GeneralNutrimentsDto.from_dict(_energy_kj)

        _fat = d.pop("fat", UNSET)
        fat: GeneralNutrimentsDto | Unset
        if isinstance(_fat, Unset):
            fat = UNSET
        else:
            fat = GeneralNutrimentsDto.from_dict(_fat)

        _saturated_fat = d.pop("saturatedFat", UNSET)
        saturated_fat: GeneralNutrimentsDto | Unset
        if isinstance(_saturated_fat, Unset):
            saturated_fat = UNSET
        else:
            saturated_fat = GeneralNutrimentsDto.from_dict(_saturated_fat)

        _carbohydrates = d.pop("carbohydrates", UNSET)
        carbohydrates: GeneralNutrimentsDto | Unset
        if isinstance(_carbohydrates, Unset):
            carbohydrates = UNSET
        else:
            carbohydrates = GeneralNutrimentsDto.from_dict(_carbohydrates)

        _sugar = d.pop("sugar", UNSET)
        sugar: GeneralNutrimentsDto | Unset
        if isinstance(_sugar, Unset):
            sugar = UNSET
        else:
            sugar = GeneralNutrimentsDto.from_dict(_sugar)

        _fiber = d.pop("fiber", UNSET)
        fiber: GeneralNutrimentsDto | Unset
        if isinstance(_fiber, Unset):
            fiber = UNSET
        else:
            fiber = GeneralNutrimentsDto.from_dict(_fiber)

        _proteins = d.pop("proteins", UNSET)
        proteins: GeneralNutrimentsDto | Unset
        if isinstance(_proteins, Unset):
            proteins = UNSET
        else:
            proteins = GeneralNutrimentsDto.from_dict(_proteins)

        _salt = d.pop("salt", UNSET)
        salt: GeneralNutrimentsDto | Unset
        if isinstance(_salt, Unset):
            salt = UNSET
        else:
            salt = GeneralNutrimentsDto.from_dict(_salt)

        _nutri_score = d.pop("nutriScore", UNSET)
        nutri_score: NutriScore | Unset
        if isinstance(_nutri_score, Unset):
            nutri_score = UNSET
        else:
            nutri_score = NutriScore(_nutri_score)

        article_nutriments_dto = cls(
            energy_kcal=energy_kcal,
            energy_kj=energy_kj,
            fat=fat,
            saturated_fat=saturated_fat,
            carbohydrates=carbohydrates,
            sugar=sugar,
            fiber=fiber,
            proteins=proteins,
            salt=salt,
            nutri_score=nutri_score,
        )

        article_nutriments_dto.additional_properties = d
        return article_nutriments_dto

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
