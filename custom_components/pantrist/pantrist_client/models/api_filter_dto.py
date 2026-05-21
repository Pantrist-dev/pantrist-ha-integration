from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.api_filter_dto_categories_item import ApiFilterDtoCategoriesItem
from ..models.api_filter_dto_language import ApiFilterDtoLanguage
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
        ingredients (list[str] | Unset): Filter by ingredient names
        author_uuid (list[str] | str | Unset): Filter by author UUID(s)
        favorites_range (OptionalRangeDto | Unset):
        total_time_range (OptionalRangeDto | Unset):
        preparation_time_range (OptionalRangeDto | Unset):
        collection_id (str | Unset): Filter by assigned collection
    """

    current_page: float | Unset = UNSET
    sort_by: ApiFilterDtoSortBy | Unset = UNSET
    search_string: str | Unset = UNSET
    should_be_public: bool | Unset = UNSET
    language: ApiFilterDtoLanguage | Unset = UNSET
    favorite_receipts: list[str] | Unset = UNSET
    categories: list[ApiFilterDtoCategoriesItem] | Unset = UNSET
    ingredients: list[str] | Unset = UNSET
    author_uuid: list[str] | str | Unset = UNSET
    favorites_range: OptionalRangeDto | Unset = UNSET
    total_time_range: OptionalRangeDto | Unset = UNSET
    preparation_time_range: OptionalRangeDto | Unset = UNSET
    collection_id: str | Unset = UNSET
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.optional_range_dto import OptionalRangeDto

        d = dict(src_dict)
        current_page = d.pop("currentPage", UNSET)

        _sort_by = d.pop("sortBy", UNSET)
        sort_by: ApiFilterDtoSortBy | Unset
        if isinstance(_sort_by, Unset):
            sort_by = UNSET
        else:
            sort_by = ApiFilterDtoSortBy(_sort_by)

        search_string = d.pop("searchString", UNSET)

        should_be_public = d.pop("shouldBePublic", UNSET)

        _language = d.pop("language", UNSET)
        language: ApiFilterDtoLanguage | Unset
        if isinstance(_language, Unset):
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
        if isinstance(_favorites_range, Unset):
            favorites_range = UNSET
        else:
            favorites_range = OptionalRangeDto.from_dict(_favorites_range)

        _total_time_range = d.pop("totalTimeRange", UNSET)
        total_time_range: OptionalRangeDto | Unset
        if isinstance(_total_time_range, Unset):
            total_time_range = UNSET
        else:
            total_time_range = OptionalRangeDto.from_dict(_total_time_range)

        _preparation_time_range = d.pop("preparationTimeRange", UNSET)
        preparation_time_range: OptionalRangeDto | Unset
        if isinstance(_preparation_time_range, Unset):
            preparation_time_range = UNSET
        else:
            preparation_time_range = OptionalRangeDto.from_dict(_preparation_time_range)

        collection_id = d.pop("collectionId", UNSET)

        api_filter_dto = cls(
            current_page=current_page,
            sort_by=sort_by,
            search_string=search_string,
            should_be_public=should_be_public,
            language=language,
            favorite_receipts=favorite_receipts,
            categories=categories,
            ingredients=ingredients,
            author_uuid=author_uuid,
            favorites_range=favorites_range,
            total_time_range=total_time_range,
            preparation_time_range=preparation_time_range,
            collection_id=collection_id,
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
