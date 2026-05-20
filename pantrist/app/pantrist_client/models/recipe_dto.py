from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.receipt_category import ReceiptCategory
from ..models.recipe_dto_language import RecipeDtoLanguage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_nutriments_dto import ArticleNutrimentsDto
    from ..models.ingredient_dto import IngredientDto
    from ..models.partial_step_dto import PartialStepDto
    from ..models.step_dto import StepDto


T = TypeVar("T", bound="RecipeDto")


@_attrs_define
class RecipeDto:
    """
    Attributes:
        uuid (str): Unique recipe identifier (UUID) Example: a3f1c5e4-1234-4f56-9abc-1234567890ab.
        name (str): Recipe name Example: Banana Pancakes.
        favorites (float): Number of times this recipe was favorited
        total_time (float): Total time in minutes
        preparation_time (float): Preparation time in minutes
        default_servings (float): Default number of servings
        servings_unit (str): Unit used for servings (e.g. Portion, g, ml) Example: Portion.
        should_be_public (bool): Whether the recipe is publicly visible
        categories (list[ReceiptCategory]): Recipe categories
        language (RecipeDtoLanguage): Recipe language (IETF locale) Example: en-US.
        show_author (bool): Whether to show the author publicly
        author_uuid (str): Author UUID
        ingredients (list[IngredientDto]): List of ingredients
        steps (list[StepDto]): Preparation steps
        image_url (str | Unset): Public image URL for the recipe
        description (str | Unset): Detailed recipe description
        cooking_time (float | Unset): Cooking time in minutes
        waiting_time (float | Unset): Waiting/resting time in minutes
        link (str | Unset): External reference link
        partial_steps (list[PartialStepDto] | Unset): Optional partial steps for grouping instructions
        copied_from_receipt_uuid (str | Unset): UUID of the recipe this one was copied from
        nutriments (ArticleNutrimentsDto | Unset):
        created_at (str | Unset): Creation date of the recipe
        updated_at (str | Unset): Last update date of the recipe
        ingredient_count (float | Unset): Number of ingredients in the recipe. Only set when requesting recipe
            pagination with current stock
        matching_ingredient_count (float | Unset): Number of ingredients in the recipe that match to the stock. Only set
            when requesting recipe pagination with current stock
    """

    uuid: str
    name: str
    favorites: float
    total_time: float
    preparation_time: float
    default_servings: float
    servings_unit: str
    should_be_public: bool
    categories: list[ReceiptCategory]
    language: RecipeDtoLanguage
    show_author: bool
    author_uuid: str
    ingredients: list[IngredientDto]
    steps: list[StepDto]
    image_url: str | Unset = UNSET
    description: str | Unset = UNSET
    cooking_time: float | Unset = UNSET
    waiting_time: float | Unset = UNSET
    link: str | Unset = UNSET
    partial_steps: list[PartialStepDto] | Unset = UNSET
    copied_from_receipt_uuid: str | Unset = UNSET
    nutriments: ArticleNutrimentsDto | Unset = UNSET
    created_at: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    ingredient_count: float | Unset = UNSET
    matching_ingredient_count: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        name = self.name

        favorites = self.favorites

        total_time = self.total_time

        preparation_time = self.preparation_time

        default_servings = self.default_servings

        servings_unit = self.servings_unit

        should_be_public = self.should_be_public

        categories = []
        for categories_item_data in self.categories:
            categories_item = categories_item_data.value
            categories.append(categories_item)

        language = self.language.value

        show_author = self.show_author

        author_uuid = self.author_uuid

        ingredients = []
        for ingredients_item_data in self.ingredients:
            ingredients_item = ingredients_item_data.to_dict()
            ingredients.append(ingredients_item)

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        image_url = self.image_url

        description = self.description

        cooking_time = self.cooking_time

        waiting_time = self.waiting_time

        link = self.link

        partial_steps: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.partial_steps, Unset):
            partial_steps = []
            for partial_steps_item_data in self.partial_steps:
                partial_steps_item = partial_steps_item_data.to_dict()
                partial_steps.append(partial_steps_item)

        copied_from_receipt_uuid = self.copied_from_receipt_uuid

        nutriments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.nutriments, Unset):
            nutriments = self.nutriments.to_dict()

        created_at = self.created_at

        updated_at = self.updated_at

        ingredient_count = self.ingredient_count

        matching_ingredient_count = self.matching_ingredient_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "favorites": favorites,
                "totalTime": total_time,
                "preparationTime": preparation_time,
                "defaultServings": default_servings,
                "servingsUnit": servings_unit,
                "shouldBePublic": should_be_public,
                "categories": categories,
                "language": language,
                "showAuthor": show_author,
                "authorUuid": author_uuid,
                "ingredients": ingredients,
                "steps": steps,
            }
        )
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if description is not UNSET:
            field_dict["description"] = description
        if cooking_time is not UNSET:
            field_dict["cookingTime"] = cooking_time
        if waiting_time is not UNSET:
            field_dict["waitingTime"] = waiting_time
        if link is not UNSET:
            field_dict["link"] = link
        if partial_steps is not UNSET:
            field_dict["partialSteps"] = partial_steps
        if copied_from_receipt_uuid is not UNSET:
            field_dict["copiedFromReceiptUuid"] = copied_from_receipt_uuid
        if nutriments is not UNSET:
            field_dict["nutriments"] = nutriments
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if ingredient_count is not UNSET:
            field_dict["ingredientCount"] = ingredient_count
        if matching_ingredient_count is not UNSET:
            field_dict["matchingIngredientCount"] = matching_ingredient_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_nutriments_dto import ArticleNutrimentsDto
        from ..models.ingredient_dto import IngredientDto
        from ..models.partial_step_dto import PartialStepDto
        from ..models.step_dto import StepDto

        d = dict(src_dict)
        uuid = d.pop("uuid")

        name = d.pop("name")

        favorites = d.pop("favorites")

        total_time = d.pop("totalTime")

        preparation_time = d.pop("preparationTime")

        default_servings = d.pop("defaultServings")

        servings_unit = d.pop("servingsUnit")

        should_be_public = d.pop("shouldBePublic")

        categories = []
        _categories = d.pop("categories")
        for categories_item_data in _categories:
            categories_item = ReceiptCategory(categories_item_data)

            categories.append(categories_item)

        language = RecipeDtoLanguage(d.pop("language"))

        show_author = d.pop("showAuthor")

        author_uuid = d.pop("authorUuid")

        ingredients = []
        _ingredients = d.pop("ingredients")
        for ingredients_item_data in _ingredients:
            ingredients_item = IngredientDto.from_dict(ingredients_item_data)

            ingredients.append(ingredients_item)

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = StepDto.from_dict(steps_item_data)

            steps.append(steps_item)

        image_url = d.pop("imageUrl", UNSET)

        description = d.pop("description", UNSET)

        cooking_time = d.pop("cookingTime", UNSET)

        waiting_time = d.pop("waitingTime", UNSET)

        link = d.pop("link", UNSET)

        _partial_steps = d.pop("partialSteps", UNSET)
        partial_steps: list[PartialStepDto] | Unset = UNSET
        if _partial_steps is not UNSET:
            partial_steps = []
            for partial_steps_item_data in _partial_steps:
                partial_steps_item = PartialStepDto.from_dict(partial_steps_item_data)

                partial_steps.append(partial_steps_item)

        copied_from_receipt_uuid = d.pop("copiedFromReceiptUuid", UNSET)

        _nutriments = d.pop("nutriments", UNSET)
        nutriments: ArticleNutrimentsDto | Unset
        if isinstance(_nutriments, Unset):
            nutriments = UNSET
        else:
            nutriments = ArticleNutrimentsDto.from_dict(_nutriments)

        created_at = d.pop("createdAt", UNSET)

        updated_at = d.pop("updatedAt", UNSET)

        ingredient_count = d.pop("ingredientCount", UNSET)

        matching_ingredient_count = d.pop("matchingIngredientCount", UNSET)

        recipe_dto = cls(
            uuid=uuid,
            name=name,
            favorites=favorites,
            total_time=total_time,
            preparation_time=preparation_time,
            default_servings=default_servings,
            servings_unit=servings_unit,
            should_be_public=should_be_public,
            categories=categories,
            language=language,
            show_author=show_author,
            author_uuid=author_uuid,
            ingredients=ingredients,
            steps=steps,
            image_url=image_url,
            description=description,
            cooking_time=cooking_time,
            waiting_time=waiting_time,
            link=link,
            partial_steps=partial_steps,
            copied_from_receipt_uuid=copied_from_receipt_uuid,
            nutriments=nutriments,
            created_at=created_at,
            updated_at=updated_at,
            ingredient_count=ingredient_count,
            matching_ingredient_count=matching_ingredient_count,
        )

        recipe_dto.additional_properties = d
        return recipe_dto

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
