from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.allergen import Allergen
from ..models.receipt_category import ReceiptCategory
from ..models.recipe_parsing_result_dto_language import RecipeParsingResultDtoLanguage
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_nutriments_dto import ArticleNutrimentsDto
    from ..models.ingredient_dto import IngredientDto
    from ..models.partial_step_dto import PartialStepDto
    from ..models.recipe_source_dto import RecipeSourceDto
    from ..models.step_dto import StepDto
    from ..models.substitution_suggestion_dto import SubstitutionSuggestionDto


T = TypeVar("T", bound="RecipeParsingResultDto")


@_attrs_define
class RecipeParsingResultDto:
    """
    Attributes:
        uuid (str): Unique recipe identifier (UUID) Example: a3f1c5e4-1234-4f56-9abc-1234567890ab.
        name (str): Recipe name Example: Banana Pancakes.
        total_time (float): Total time in minutes
        preparation_time (float): Preparation time in minutes
        default_servings (float): Default number of servings
        servings_unit (str): Unit used for servings (e.g. Portion, g, ml) Example: Portion.
        should_be_public (bool): Whether the recipe is publicly visible inside the app. Imports are kept out of the
            sitemap and carry robots: noindex regardless, so this never exposes somebody else's post to a search engine.
        categories (list[ReceiptCategory]): Recipe categories
        language (RecipeParsingResultDtoLanguage): Recipe language (IETF locale) Example: en-US.
        show_author (bool): Whether to show the author publicly
        author_uuid (str): Author UUID
        ingredients (list[IngredientDto]): List of ingredients
        steps (list[StepDto]): Preparation steps
        image_url (str | Unset): Public image URL for the recipe
        favorites (float | Unset): Number of times this recipe was favorited. Read-only — any value sent on
            create/update is ignored; it is computed from likes.
        description (str | Unset): Detailed recipe description
        cooking_time (float | Unset): Cooking time in minutes
        waiting_time (float | Unset): Waiting/resting time in minutes
        allergens (list[Allergen] | Unset): Allergens contained in the recipe (EU 14). Extracted by the recipe parser
            and/or derived from ingredients on save; clients should treat this as best-effort guidance, not a legal
            declaration.
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
        missing_ingredients (list[str] | Unset): Names of the recipe ingredients that are NOT covered by the current
            stock (pantry staples such as salt, oil or water are excluded and always treated as available). Only set when
            filtering by ingredients.
        substitutable_count (float | Unset): Number of missing ingredients the user could substitute from their pantry.
            Counted separately from matches — show as a softer "can substitute" state, not as "have it". Only set when
            filtering by ingredients and a substitution applies.
        substitutable_ingredients (list[str] | Unset): Names of the recipe ingredients that are not in stock but covered
            by a curated substitution from the pantry. These are excluded from missingIngredients. Only set when filtering
            by ingredients.
        substitutions (list[SubstitutionSuggestionDto] | Unset): Concrete "use X instead of Y" suggestions for the
            substitutable ingredients. Only set when filtering by ingredients and a substitution applies.
        source (RecipeSourceDto | Unset):
        image_base_64 (str | Unset): Image in base64 format
        image_mime_type (str | Unset): Image mime type Example: image/jpeg.
    """

    uuid: str
    name: str
    total_time: float
    preparation_time: float
    default_servings: float
    servings_unit: str
    should_be_public: bool
    categories: list[ReceiptCategory]
    language: RecipeParsingResultDtoLanguage
    show_author: bool
    author_uuid: str
    ingredients: list[IngredientDto]
    steps: list[StepDto]
    image_url: str | Unset = UNSET
    favorites: float | Unset = UNSET
    description: str | Unset = UNSET
    cooking_time: float | Unset = UNSET
    waiting_time: float | Unset = UNSET
    allergens: list[Allergen] | Unset = UNSET
    link: str | Unset = UNSET
    partial_steps: list[PartialStepDto] | Unset = UNSET
    copied_from_receipt_uuid: str | Unset = UNSET
    nutriments: ArticleNutrimentsDto | Unset = UNSET
    created_at: str | Unset = UNSET
    updated_at: str | Unset = UNSET
    ingredient_count: float | Unset = UNSET
    matching_ingredient_count: float | Unset = UNSET
    missing_ingredients: list[str] | Unset = UNSET
    substitutable_count: float | Unset = UNSET
    substitutable_ingredients: list[str] | Unset = UNSET
    substitutions: list[SubstitutionSuggestionDto] | Unset = UNSET
    source: RecipeSourceDto | Unset = UNSET
    image_base_64: str | Unset = UNSET
    image_mime_type: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = self.uuid

        name = self.name

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

        favorites = self.favorites

        description = self.description

        cooking_time = self.cooking_time

        waiting_time = self.waiting_time

        allergens: list[str] | Unset = UNSET
        if not isinstance(self.allergens, Unset):
            allergens = []
            for allergens_item_data in self.allergens:
                allergens_item = allergens_item_data.value
                allergens.append(allergens_item)

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

        missing_ingredients: list[str] | Unset = UNSET
        if not isinstance(self.missing_ingredients, Unset):
            missing_ingredients = self.missing_ingredients

        substitutable_count = self.substitutable_count

        substitutable_ingredients: list[str] | Unset = UNSET
        if not isinstance(self.substitutable_ingredients, Unset):
            substitutable_ingredients = self.substitutable_ingredients

        substitutions: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.substitutions, Unset):
            substitutions = []
            for substitutions_item_data in self.substitutions:
                substitutions_item = substitutions_item_data.to_dict()
                substitutions.append(substitutions_item)

        source: dict[str, Any] | Unset = UNSET
        if not isinstance(self.source, Unset):
            source = self.source.to_dict()

        image_base_64 = self.image_base_64

        image_mime_type = self.image_mime_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
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
        if favorites is not UNSET:
            field_dict["favorites"] = favorites
        if description is not UNSET:
            field_dict["description"] = description
        if cooking_time is not UNSET:
            field_dict["cookingTime"] = cooking_time
        if waiting_time is not UNSET:
            field_dict["waitingTime"] = waiting_time
        if allergens is not UNSET:
            field_dict["allergens"] = allergens
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
        if missing_ingredients is not UNSET:
            field_dict["missingIngredients"] = missing_ingredients
        if substitutable_count is not UNSET:
            field_dict["substitutableCount"] = substitutable_count
        if substitutable_ingredients is not UNSET:
            field_dict["substitutableIngredients"] = substitutable_ingredients
        if substitutions is not UNSET:
            field_dict["substitutions"] = substitutions
        if source is not UNSET:
            field_dict["source"] = source
        if image_base_64 is not UNSET:
            field_dict["imageBase64"] = image_base_64
        if image_mime_type is not UNSET:
            field_dict["imageMimeType"] = image_mime_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_nutriments_dto import ArticleNutrimentsDto  # noqa: PLC0415
        from ..models.ingredient_dto import IngredientDto  # noqa: PLC0415
        from ..models.partial_step_dto import PartialStepDto  # noqa: PLC0415
        from ..models.recipe_source_dto import RecipeSourceDto  # noqa: PLC0415
        from ..models.step_dto import StepDto  # noqa: PLC0415
        from ..models.substitution_suggestion_dto import SubstitutionSuggestionDto  # noqa: PLC0415

        d = dict(src_dict)
        uuid = d.pop("uuid")

        name = d.pop("name")

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

        language = RecipeParsingResultDtoLanguage(d.pop("language"))

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

        favorites = d.pop("favorites", UNSET)

        description = d.pop("description", UNSET)

        cooking_time = d.pop("cookingTime", UNSET)

        waiting_time = d.pop("waitingTime", UNSET)

        _allergens = d.pop("allergens", UNSET)
        allergens: list[Allergen] | Unset = UNSET
        if _allergens is not UNSET:
            allergens = []
            for allergens_item_data in _allergens:
                allergens_item = Allergen(allergens_item_data)

                allergens.append(allergens_item)

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
        if isinstance(_nutriments, Unset) or _nutriments is None:
            nutriments = UNSET
        else:
            nutriments = ArticleNutrimentsDto.from_dict(_nutriments)

        created_at = d.pop("createdAt", UNSET)

        updated_at = d.pop("updatedAt", UNSET)

        ingredient_count = d.pop("ingredientCount", UNSET)

        matching_ingredient_count = d.pop("matchingIngredientCount", UNSET)

        missing_ingredients = cast(list[str], d.pop("missingIngredients", UNSET))

        substitutable_count = d.pop("substitutableCount", UNSET)

        substitutable_ingredients = cast(list[str], d.pop("substitutableIngredients", UNSET))

        _substitutions = d.pop("substitutions", UNSET)
        substitutions: list[SubstitutionSuggestionDto] | Unset = UNSET
        if _substitutions is not UNSET:
            substitutions = []
            for substitutions_item_data in _substitutions:
                substitutions_item = SubstitutionSuggestionDto.from_dict(substitutions_item_data)

                substitutions.append(substitutions_item)

        _source = d.pop("source", UNSET)
        source: RecipeSourceDto | Unset
        if isinstance(_source, Unset) or _source is None:
            source = UNSET
        else:
            source = RecipeSourceDto.from_dict(_source)

        image_base_64 = d.pop("imageBase64", UNSET)

        image_mime_type = d.pop("imageMimeType", UNSET)

        recipe_parsing_result_dto = cls(
            uuid=uuid,
            name=name,
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
            favorites=favorites,
            description=description,
            cooking_time=cooking_time,
            waiting_time=waiting_time,
            allergens=allergens,
            link=link,
            partial_steps=partial_steps,
            copied_from_receipt_uuid=copied_from_receipt_uuid,
            nutriments=nutriments,
            created_at=created_at,
            updated_at=updated_at,
            ingredient_count=ingredient_count,
            matching_ingredient_count=matching_ingredient_count,
            missing_ingredients=missing_ingredients,
            substitutable_count=substitutable_count,
            substitutable_ingredients=substitutable_ingredients,
            substitutions=substitutions,
            source=source,
            image_base_64=image_base_64,
            image_mime_type=image_mime_type,
        )

        recipe_parsing_result_dto.additional_properties = d
        return recipe_parsing_result_dto

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
