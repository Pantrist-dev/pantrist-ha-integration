from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.api_filter_dto_categories_item import ApiFilterDtoCategoriesItem
from ..models.api_filter_dto_dietary_styles_item import ApiFilterDtoDietaryStylesItem
from ..models.api_filter_dto_exclude_allergens_item import ApiFilterDtoExcludeAllergensItem
from ..models.api_filter_dto_language import ApiFilterDtoLanguage
from ..models.api_filter_dto_pantry_filter import ApiFilterDtoPantryFilter
from ..models.api_filter_dto_sort_by import ApiFilterDtoSortBy
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.optional_range_dto import OptionalRangeDto


T = TypeVar("T", bound="ApiFilterDto")


@_attrs_define
class ApiFilterDto:
    """
    Attributes:
        current_page (float | Unset): Current page (1-based) Example: 1.
        sort_by (ApiFilterDtoSortBy | Unset): Sort order Example: AlphabeticalAsc.
        search_string (str | Unset): Search string (name, description, ingredients) Example: pancake.
        should_be_public (bool | Unset): Only public recipes
        language (ApiFilterDtoLanguage | Unset):  Example: en-US.
        favorite_receipts (list[str] | Unset): Filter by favorite recipe UUIDs
        categories (list[ApiFilterDtoCategoriesItem] | Unset): Filter by categories
        ingredients (list[str] | Unset): Legacy: the pantry as ingredient names. Use `pantryFilter` (plus `listIds`)
            instead, which reads the pantry server-side with its already-resolved ingredient ids. Every name sent here is
            resolved per request, and the resolver ends in a language model, so a pantry of a thousand items costs a
            thousand resolves on every call. Still honoured for app versions in the field and for local-only users, who have
            no server-side pantry. When set, it wins over `pantryFilter`.
        pantry_filter (ApiFilterDtoPantryFilter | Unset): Opt-in to server-side pantry matching. Setting this field
            tells the server to hydrate the authenticated user's pantry items (across all of their lists) and score recipes
            against them — the app does not need to ship a 50–200 item array on every request. `all` uses every pantry item
            the user currently has. `expiring` keeps only items whose earliest best-before date is at most 14 days away
            (already expired or close to it), so the match prioritises ingredients the user should use up next. Mutually
            exclusive with `ingredients` — an explicit ingredients array always wins, and this field is ignored when no user
            is attached. Example: all.
        list_ids (list[str] | Unset): Restrict the `pantryFilter` hydration to a subset of the user's lists. When the
            app is showing a single household list, send `[currentListId]` so "fitting recipes" / "use-up-soon" only
            consider that household's pantry; in all-lists mode send every list id (or omit to fall back to all). Ignored
            when `pantryFilter` is unset or no user is attached. Ids the caller does not own are silently dropped server-
            side.
        author_uuid (list[str] | str | Unset): Filter by author UUID(s)
        favorites_range (OptionalRangeDto | Unset):
        total_time_range (OptionalRangeDto | Unset):
        preparation_time_range (OptionalRangeDto | Unset):
        collection_id (str | Unset): Filter by assigned collection
        dietary_styles (list[ApiFilterDtoDietaryStylesItem] | Unset): Only recipes that match EVERY selected dietary
            style (AND). Dietary styles are a subset of the recipe categories (e.g. Vegan, Vegetarian, Keto, GlutenFree,
            HighProtein). The user setting "vegan + high protein" should surface vegan recipes that are also high-protein —
            a match-any filter here would leak non-vegan recipes whenever any other style happened to match.
        exclude_allergens (list[ApiFilterDtoExcludeAllergensItem] | Unset): Exclude recipes that contain ANY of these
            allergens. Recipes whose allergens are unknown (null) are NOT excluded.
        main_courses_only (bool | Unset): Leave out recipes whose categories say they are not a meal of their own
            (dessert, breakfast, snack, drink, side, …), unless they also carry a meal category (lunch, dinner, soup, …). A
            recipe without categories is kept.
    """

    current_page: float | Unset = UNSET
    sort_by: ApiFilterDtoSortBy | Unset = UNSET
    search_string: str | Unset = UNSET
    should_be_public: bool | Unset = UNSET
    language: ApiFilterDtoLanguage | Unset = UNSET
    favorite_receipts: list[str] | Unset = UNSET
    categories: list[ApiFilterDtoCategoriesItem] | Unset = UNSET
    ingredients: list[str] | Unset = UNSET
    pantry_filter: ApiFilterDtoPantryFilter | Unset = UNSET
    list_ids: list[str] | Unset = UNSET
    author_uuid: list[str] | str | Unset = UNSET
    favorites_range: OptionalRangeDto | Unset = UNSET
    total_time_range: OptionalRangeDto | Unset = UNSET
    preparation_time_range: OptionalRangeDto | Unset = UNSET
    collection_id: str | Unset = UNSET
    dietary_styles: list[ApiFilterDtoDietaryStylesItem] | Unset = UNSET
    exclude_allergens: list[ApiFilterDtoExcludeAllergensItem] | Unset = UNSET
    main_courses_only: bool | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        current_page = self.current_page

        sort_by: str | Unset = UNSET
        if not isinstance(self.sort_by, Unset):
            sort_by = self.sort_by.value

        search_string = self.search_string

        should_be_public = self.should_be_public

        language: str | Unset = UNSET
        if not isinstance(self.language, Unset):
            language = self.language.value

        favorite_receipts: list[str] | Unset = UNSET
        if not isinstance(self.favorite_receipts, Unset):
            favorite_receipts = self.favorite_receipts

        categories: list[str] | Unset = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for categories_item_data in self.categories:
                categories_item = categories_item_data.value
                categories.append(categories_item)

        ingredients: list[str] | Unset = UNSET
        if not isinstance(self.ingredients, Unset):
            ingredients = self.ingredients

        pantry_filter: str | Unset = UNSET
        if not isinstance(self.pantry_filter, Unset):
            pantry_filter = self.pantry_filter.value

        list_ids: list[str] | Unset = UNSET
        if not isinstance(self.list_ids, Unset):
            list_ids = self.list_ids

        author_uuid: list[str] | str | Unset
        if isinstance(self.author_uuid, Unset):
            author_uuid = UNSET
        elif isinstance(self.author_uuid, list):
            author_uuid = self.author_uuid

        else:
            author_uuid = self.author_uuid

        favorites_range: dict[str, Any] | Unset = UNSET
        if not isinstance(self.favorites_range, Unset):
            favorites_range = self.favorites_range.to_dict()

        total_time_range: dict[str, Any] | Unset = UNSET
        if not isinstance(self.total_time_range, Unset):
            total_time_range = self.total_time_range.to_dict()

        preparation_time_range: dict[str, Any] | Unset = UNSET
        if not isinstance(self.preparation_time_range, Unset):
            preparation_time_range = self.preparation_time_range.to_dict()

        collection_id = self.collection_id

        dietary_styles: list[str] | Unset = UNSET
        if not isinstance(self.dietary_styles, Unset):
            dietary_styles = []
            for dietary_styles_item_data in self.dietary_styles:
                dietary_styles_item = dietary_styles_item_data.value
                dietary_styles.append(dietary_styles_item)

        exclude_allergens: list[str] | Unset = UNSET
        if not isinstance(self.exclude_allergens, Unset):
            exclude_allergens = []
            for exclude_allergens_item_data in self.exclude_allergens:
                exclude_allergens_item = exclude_allergens_item_data.value
                exclude_allergens.append(exclude_allergens_item)

        main_courses_only = self.main_courses_only

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if current_page is not UNSET:
            field_dict["currentPage"] = current_page
        if sort_by is not UNSET:
            field_dict["sortBy"] = sort_by
        if search_string is not UNSET:
            field_dict["searchString"] = search_string
        if should_be_public is not UNSET:
            field_dict["shouldBePublic"] = should_be_public
        if language is not UNSET:
            field_dict["language"] = language
        if favorite_receipts is not UNSET:
            field_dict["favoriteReceipts"] = favorite_receipts
        if categories is not UNSET:
            field_dict["categories"] = categories
        if ingredients is not UNSET:
            field_dict["ingredients"] = ingredients
        if pantry_filter is not UNSET:
            field_dict["pantryFilter"] = pantry_filter
        if list_ids is not UNSET:
            field_dict["listIds"] = list_ids
        if author_uuid is not UNSET:
            field_dict["authorUuid"] = author_uuid
        if favorites_range is not UNSET:
            field_dict["favoritesRange"] = favorites_range
        if total_time_range is not UNSET:
            field_dict["totalTimeRange"] = total_time_range
        if preparation_time_range is not UNSET:
            field_dict["preparationTimeRange"] = preparation_time_range
        if collection_id is not UNSET:
            field_dict["collectionId"] = collection_id
        if dietary_styles is not UNSET:
            field_dict["dietaryStyles"] = dietary_styles
        if exclude_allergens is not UNSET:
            field_dict["excludeAllergens"] = exclude_allergens
        if main_courses_only is not UNSET:
            field_dict["mainCoursesOnly"] = main_courses_only

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.optional_range_dto import OptionalRangeDto  # noqa: PLC0415

        d = dict(src_dict)
        current_page = d.pop("currentPage", UNSET)

        _sort_by = d.pop("sortBy", UNSET)
        sort_by: ApiFilterDtoSortBy | Unset
        if isinstance(_sort_by, Unset) or _sort_by is None or _sort_by == "":
            sort_by = UNSET
        else:
            sort_by = ApiFilterDtoSortBy(_sort_by)

        search_string = d.pop("searchString", UNSET)

        should_be_public = d.pop("shouldBePublic", UNSET)

        _language = d.pop("language", UNSET)
        language: ApiFilterDtoLanguage | Unset
        if isinstance(_language, Unset) or _language is None or _language == "":
            language = UNSET
        else:
            language = ApiFilterDtoLanguage(_language)

        favorite_receipts = cast(list[str], d.pop("favoriteReceipts", UNSET))

        _categories = d.pop("categories", UNSET)
        categories: list[ApiFilterDtoCategoriesItem] | Unset = UNSET
        if _categories is not UNSET:
            categories = []
            for categories_item_data in _categories:
                categories_item = ApiFilterDtoCategoriesItem(categories_item_data)

                categories.append(categories_item)

        ingredients = cast(list[str], d.pop("ingredients", UNSET))

        _pantry_filter = d.pop("pantryFilter", UNSET)
        pantry_filter: ApiFilterDtoPantryFilter | Unset
        if isinstance(_pantry_filter, Unset) or _pantry_filter is None or _pantry_filter == "":
            pantry_filter = UNSET
        else:
            pantry_filter = ApiFilterDtoPantryFilter(_pantry_filter)

        list_ids = cast(list[str], d.pop("listIds", UNSET))

        def _parse_author_uuid(data: object) -> list[str] | str | Unset:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                author_uuid_type_1 = cast(list[str], data)

                return author_uuid_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | str | Unset, data)

        author_uuid = _parse_author_uuid(d.pop("authorUuid", UNSET))

        _favorites_range = d.pop("favoritesRange", UNSET)
        favorites_range: OptionalRangeDto | Unset
        if isinstance(_favorites_range, Unset) or _favorites_range is None:
            favorites_range = UNSET
        else:
            favorites_range = OptionalRangeDto.from_dict(_favorites_range)

        _total_time_range = d.pop("totalTimeRange", UNSET)
        total_time_range: OptionalRangeDto | Unset
        if isinstance(_total_time_range, Unset) or _total_time_range is None:
            total_time_range = UNSET
        else:
            total_time_range = OptionalRangeDto.from_dict(_total_time_range)

        _preparation_time_range = d.pop("preparationTimeRange", UNSET)
        preparation_time_range: OptionalRangeDto | Unset
        if isinstance(_preparation_time_range, Unset) or _preparation_time_range is None:
            preparation_time_range = UNSET
        else:
            preparation_time_range = OptionalRangeDto.from_dict(_preparation_time_range)

        collection_id = d.pop("collectionId", UNSET)

        _dietary_styles = d.pop("dietaryStyles", UNSET)
        dietary_styles: list[ApiFilterDtoDietaryStylesItem] | Unset = UNSET
        if _dietary_styles is not UNSET:
            dietary_styles = []
            for dietary_styles_item_data in _dietary_styles:
                dietary_styles_item = ApiFilterDtoDietaryStylesItem(dietary_styles_item_data)

                dietary_styles.append(dietary_styles_item)

        _exclude_allergens = d.pop("excludeAllergens", UNSET)
        exclude_allergens: list[ApiFilterDtoExcludeAllergensItem] | Unset = UNSET
        if _exclude_allergens is not UNSET:
            exclude_allergens = []
            for exclude_allergens_item_data in _exclude_allergens:
                exclude_allergens_item = ApiFilterDtoExcludeAllergensItem(exclude_allergens_item_data)

                exclude_allergens.append(exclude_allergens_item)

        main_courses_only = d.pop("mainCoursesOnly", UNSET)

        api_filter_dto = cls(
            current_page=current_page,
            sort_by=sort_by,
            search_string=search_string,
            should_be_public=should_be_public,
            language=language,
            favorite_receipts=favorite_receipts,
            categories=categories,
            ingredients=ingredients,
            pantry_filter=pantry_filter,
            list_ids=list_ids,
            author_uuid=author_uuid,
            favorites_range=favorites_range,
            total_time_range=total_time_range,
            preparation_time_range=preparation_time_range,
            collection_id=collection_id,
            dietary_styles=dietary_styles,
            exclude_allergens=exclude_allergens,
            main_courses_only=main_courses_only,
        )

        api_filter_dto.additional_properties = d
        return api_filter_dto

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
