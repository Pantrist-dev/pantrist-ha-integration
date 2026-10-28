from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.allergen import Allergen
from ..models.discount_type import DiscountType
from ..models.minimum_amount_mode import MinimumAmountMode
from ..models.price_type import PriceType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto
    from ..models.article_dto_price_per_market_type_0 import ArticleDtoPricePerMarketType0
    from ..models.article_nutriments_dto import ArticleNutrimentsDto
    from ..models.auto_reduce_config_dto import AutoReduceConfigDto
    from ..models.household_details_dto import HouseholdDetailsDto
    from ..models.item_pantry_settings_dto import ItemPantrySettingsDto
    from ..models.weighing_dto import WeighingDto


T = TypeVar("T", bound="ArticleDto")


@_attrs_define
class ArticleDto:
    """
    Attributes:
        uuid (str):
        name (str):
        category_uuid (str):
        content_volume (float):
        unit_id (str):
        amount (float):
        manage_minimum_amount (bool):
        minimum_amount (float):
        minimum_amount_mode (MinimumAmountMode): What `minimumAmount` counts. 'packages' (the default): whole packages.
            'content': the content of the packages in the article's unit (`amount * contentVolume`), e.g. 3 rolls out of
            packs of 8. The shopping list still gets whole packages.
        amount_to_buy (float):
        price_type (PriceType):
        discount_type (DiscountType):
        pantry_settings (ItemPantrySettingsDto):
        brand (None | str | Unset):
        barcode (list[str] | None | str | Unset):
        notes (None | str | Unset):
        supermarket_id (list[str] | None | str | Unset):
        disable_min_amount (bool | None | Unset):
        merge_different_content (bool | None | Unset): Whether two entries of this article that differ only in
            contentVolume count as the same thing. null means the user has not been asked yet.
        placeholder_for_category_uuid (None | str | Unset): Set by the server on the auto-managed placeholder row it
            keeps on the shopping list for a category with a configured minimum stock; holds that category's uuid. Null on
            every item a user created. Clients may render such a row as a category placeholder (e.g. with the translated
            category label) rather than a concrete article. Strictly read-only: the server keeps whatever is already stored
            and ignores the value a write supplies, so omitting it never clears the marker.
        price (float | None | Unset):
        deposit (float | None | Unset):
        discount (float | None | Unset):
        discount_per_unit_or_total (None | PriceType | Unset):
        coupon_name (None | str | Unset):
        coupon_expiration_date (None | str | Unset):
        image_url (None | str | Unset):
        additional_image_urls (list[str] | None | Unset): Additional product photo URLs, ordered. imageUrl is the
            primary photo.
        predefined_pantry (None | str | Unset):
        default_best_before_days (float | None | Unset):
        purchase_date (None | str | Unset):
        last_inventory_date (None | str | Unset):
        last_modified (float | None | Unset):
        tags (list[str] | None | Unset):
        allergens (list[Allergen] | None | Unset): Allergens (EU 14) this item contains. Auto-detected from the name on
            add and overridable by the client. Best-effort guidance, not a legal declaration.
        ingredient_id (None | str | Unset): Server-derived canonical ingredient id, resolved from the name on add.
            Shares identity with recipe ingredients for matching and de-duplication. Read-only; null when unresolved.
        nutriments (ArticleNutrimentsDto | Unset):
        household_details (HouseholdDetailsDto | Unset):
        weighing (WeighingDto | Unset):
        complex_best_before_data (ArticleCatalogBestBeforeDatesDto | Unset):
        generic_price_from_catalog (float | None | Unset):
        price_per_market (ArticleDtoPricePerMarketType0 | None | Unset):
        list_id (str | Unset): The list this item belongs to. Populated by the server on cross-list endpoints.
        auto_reduce (AutoReduceConfigDto | Unset):
    """

    uuid: str
    name: str
    category_uuid: str
    content_volume: float
    unit_id: str
    amount: float
    manage_minimum_amount: bool
    minimum_amount: float
    minimum_amount_mode: MinimumAmountMode
    amount_to_buy: float
    price_type: PriceType
    discount_type: DiscountType
    pantry_settings: ItemPantrySettingsDto
    brand: None | str | Unset = UNSET
    barcode: list[str] | None | str | Unset = UNSET
    notes: None | str | Unset = UNSET
    supermarket_id: list[str] | None | str | Unset = UNSET
    disable_min_amount: bool | None | Unset = UNSET
    merge_different_content: bool | None | Unset = UNSET
    placeholder_for_category_uuid: None | str | Unset = UNSET
    price: float | None | Unset = UNSET
    deposit: float | None | Unset = UNSET
    discount: float | None | Unset = UNSET
    discount_per_unit_or_total: None | PriceType | Unset = UNSET
    coupon_name: None | str | Unset = UNSET
    coupon_expiration_date: None | str | Unset = UNSET
    image_url: None | str | Unset = UNSET
    additional_image_urls: list[str] | None | Unset = UNSET
    predefined_pantry: None | str | Unset = UNSET
    default_best_before_days: float | None | Unset = UNSET
    purchase_date: None | str | Unset = UNSET
    last_inventory_date: None | str | Unset = UNSET
    last_modified: float | None | Unset = UNSET
    tags: list[str] | None | Unset = UNSET
    allergens: list[Allergen] | None | Unset = UNSET
    ingredient_id: None | str | Unset = UNSET
    nutriments: ArticleNutrimentsDto | Unset = UNSET
    household_details: HouseholdDetailsDto | Unset = UNSET
    weighing: WeighingDto | Unset = UNSET
    complex_best_before_data: ArticleCatalogBestBeforeDatesDto | Unset = UNSET
    generic_price_from_catalog: float | None | Unset = UNSET
    price_per_market: ArticleDtoPricePerMarketType0 | None | Unset = UNSET
    list_id: str | Unset = UNSET
    auto_reduce: AutoReduceConfigDto | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.article_dto_price_per_market_type_0 import ArticleDtoPricePerMarketType0  # noqa: PLC0415

        uuid = self.uuid

        name = self.name

        category_uuid = self.category_uuid

        content_volume = self.content_volume

        unit_id = self.unit_id

        amount = self.amount

        manage_minimum_amount = self.manage_minimum_amount

        minimum_amount = self.minimum_amount

        minimum_amount_mode = self.minimum_amount_mode.value

        amount_to_buy = self.amount_to_buy

        price_type = self.price_type.value

        discount_type = self.discount_type.value

        pantry_settings = self.pantry_settings.to_dict()

        brand: None | str | Unset
        if isinstance(self.brand, Unset):
            brand = UNSET
        else:
            brand = self.brand

        barcode: list[str] | None | str | Unset
        if isinstance(self.barcode, Unset):
            barcode = UNSET
        elif isinstance(self.barcode, list):
            barcode = self.barcode

        else:
            barcode = self.barcode

        notes: None | str | Unset
        if isinstance(self.notes, Unset):
            notes = UNSET
        else:
            notes = self.notes

        supermarket_id: list[str] | None | str | Unset
        if isinstance(self.supermarket_id, Unset):
            supermarket_id = UNSET
        elif isinstance(self.supermarket_id, list):
            supermarket_id = self.supermarket_id

        else:
            supermarket_id = self.supermarket_id

        disable_min_amount: bool | None | Unset
        if isinstance(self.disable_min_amount, Unset):
            disable_min_amount = UNSET
        else:
            disable_min_amount = self.disable_min_amount

        merge_different_content: bool | None | Unset
        if isinstance(self.merge_different_content, Unset):
            merge_different_content = UNSET
        else:
            merge_different_content = self.merge_different_content

        placeholder_for_category_uuid: None | str | Unset
        if isinstance(self.placeholder_for_category_uuid, Unset):
            placeholder_for_category_uuid = UNSET
        else:
            placeholder_for_category_uuid = self.placeholder_for_category_uuid

        price: float | None | Unset
        if isinstance(self.price, Unset):
            price = UNSET
        else:
            price = self.price

        deposit: float | None | Unset
        if isinstance(self.deposit, Unset):
            deposit = UNSET
        else:
            deposit = self.deposit

        discount: float | None | Unset
        if isinstance(self.discount, Unset):
            discount = UNSET
        else:
            discount = self.discount

        discount_per_unit_or_total: None | str | Unset
        if isinstance(self.discount_per_unit_or_total, Unset):
            discount_per_unit_or_total = UNSET
        elif isinstance(self.discount_per_unit_or_total, PriceType):
            discount_per_unit_or_total = self.discount_per_unit_or_total.value
        else:
            discount_per_unit_or_total = self.discount_per_unit_or_total

        coupon_name: None | str | Unset
        if isinstance(self.coupon_name, Unset):
            coupon_name = UNSET
        else:
            coupon_name = self.coupon_name

        coupon_expiration_date: None | str | Unset
        if isinstance(self.coupon_expiration_date, Unset):
            coupon_expiration_date = UNSET
        else:
            coupon_expiration_date = self.coupon_expiration_date

        image_url: None | str | Unset
        if isinstance(self.image_url, Unset):
            image_url = UNSET
        else:
            image_url = self.image_url

        additional_image_urls: list[str] | None | Unset
        if isinstance(self.additional_image_urls, Unset):
            additional_image_urls = UNSET
        elif isinstance(self.additional_image_urls, list):
            additional_image_urls = self.additional_image_urls

        else:
            additional_image_urls = self.additional_image_urls

        predefined_pantry: None | str | Unset
        if isinstance(self.predefined_pantry, Unset):
            predefined_pantry = UNSET
        else:
            predefined_pantry = self.predefined_pantry

        default_best_before_days: float | None | Unset
        if isinstance(self.default_best_before_days, Unset):
            default_best_before_days = UNSET
        else:
            default_best_before_days = self.default_best_before_days

        purchase_date: None | str | Unset
        if isinstance(self.purchase_date, Unset):
            purchase_date = UNSET
        else:
            purchase_date = self.purchase_date

        last_inventory_date: None | str | Unset
        if isinstance(self.last_inventory_date, Unset):
            last_inventory_date = UNSET
        else:
            last_inventory_date = self.last_inventory_date

        last_modified: float | None | Unset
        if isinstance(self.last_modified, Unset):
            last_modified = UNSET
        else:
            last_modified = self.last_modified

        tags: list[str] | None | Unset
        if isinstance(self.tags, Unset):
            tags = UNSET
        elif isinstance(self.tags, list):
            tags = self.tags

        else:
            tags = self.tags

        allergens: list[str] | None | Unset
        if isinstance(self.allergens, Unset):
            allergens = UNSET
        elif isinstance(self.allergens, list):
            allergens = []
            for allergens_type_0_item_data in self.allergens:
                allergens_type_0_item = allergens_type_0_item_data.value
                allergens.append(allergens_type_0_item)

        else:
            allergens = self.allergens

        ingredient_id: None | str | Unset
        if isinstance(self.ingredient_id, Unset):
            ingredient_id = UNSET
        else:
            ingredient_id = self.ingredient_id

        nutriments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.nutriments, Unset):
            nutriments = self.nutriments.to_dict()

        household_details: dict[str, Any] | Unset = UNSET
        if not isinstance(self.household_details, Unset):
            household_details = self.household_details.to_dict()

        weighing: dict[str, Any] | Unset = UNSET
        if not isinstance(self.weighing, Unset):
            weighing = self.weighing.to_dict()

        complex_best_before_data: dict[str, Any] | Unset = UNSET
        if not isinstance(self.complex_best_before_data, Unset):
            complex_best_before_data = self.complex_best_before_data.to_dict()

        generic_price_from_catalog: float | None | Unset
        if isinstance(self.generic_price_from_catalog, Unset):
            generic_price_from_catalog = UNSET
        else:
            generic_price_from_catalog = self.generic_price_from_catalog

        price_per_market: dict[str, Any] | None | Unset
        if isinstance(self.price_per_market, Unset):
            price_per_market = UNSET
        elif isinstance(self.price_per_market, ArticleDtoPricePerMarketType0):
            price_per_market = self.price_per_market.to_dict()
        else:
            price_per_market = self.price_per_market

        list_id = self.list_id

        auto_reduce: dict[str, Any] | Unset = UNSET
        if not isinstance(self.auto_reduce, Unset):
            auto_reduce = self.auto_reduce.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "name": name,
                "categoryUuid": category_uuid,
                "contentVolume": content_volume,
                "unitId": unit_id,
                "amount": amount,
                "manageMinimumAmount": manage_minimum_amount,
                "minimumAmount": minimum_amount,
                "minimumAmountMode": minimum_amount_mode,
                "amountToBuy": amount_to_buy,
                "priceType": price_type,
                "discountType": discount_type,
                "pantrySettings": pantry_settings,
            }
        )
        if brand is not UNSET:
            field_dict["brand"] = brand
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if notes is not UNSET:
            field_dict["notes"] = notes
        if supermarket_id is not UNSET:
            field_dict["supermarketId"] = supermarket_id
        if disable_min_amount is not UNSET:
            field_dict["disableMinAmount"] = disable_min_amount
        if merge_different_content is not UNSET:
            field_dict["mergeDifferentContent"] = merge_different_content
        if placeholder_for_category_uuid is not UNSET:
            field_dict["placeholderForCategoryUuid"] = placeholder_for_category_uuid
        if price is not UNSET:
            field_dict["price"] = price
        if deposit is not UNSET:
            field_dict["deposit"] = deposit
        if discount is not UNSET:
            field_dict["discount"] = discount
        if discount_per_unit_or_total is not UNSET:
            field_dict["discountPerUnitOrTotal"] = discount_per_unit_or_total
        if coupon_name is not UNSET:
            field_dict["couponName"] = coupon_name
        if coupon_expiration_date is not UNSET:
            field_dict["couponExpirationDate"] = coupon_expiration_date
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if additional_image_urls is not UNSET:
            field_dict["additionalImageUrls"] = additional_image_urls
        if predefined_pantry is not UNSET:
            field_dict["predefinedPantry"] = predefined_pantry
        if default_best_before_days is not UNSET:
            field_dict["defaultBestBeforeDays"] = default_best_before_days
        if purchase_date is not UNSET:
            field_dict["purchaseDate"] = purchase_date
        if last_inventory_date is not UNSET:
            field_dict["lastInventoryDate"] = last_inventory_date
        if last_modified is not UNSET:
            field_dict["lastModified"] = last_modified
        if tags is not UNSET:
            field_dict["tags"] = tags
        if allergens is not UNSET:
            field_dict["allergens"] = allergens
        if ingredient_id is not UNSET:
            field_dict["ingredientId"] = ingredient_id
        if nutriments is not UNSET:
            field_dict["nutriments"] = nutriments
        if household_details is not UNSET:
            field_dict["householdDetails"] = household_details
        if weighing is not UNSET:
            field_dict["weighing"] = weighing
        if complex_best_before_data is not UNSET:
            field_dict["complexBestBeforeData"] = complex_best_before_data
        if generic_price_from_catalog is not UNSET:
            field_dict["genericPriceFromCatalog"] = generic_price_from_catalog
        if price_per_market is not UNSET:
            field_dict["pricePerMarket"] = price_per_market
        if list_id is not UNSET:
            field_dict["listId"] = list_id
        if auto_reduce is not UNSET:
            field_dict["autoReduce"] = auto_reduce

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.article_catalog_best_before_dates_dto import ArticleCatalogBestBeforeDatesDto  # noqa: PLC0415
        from ..models.article_dto_price_per_market_type_0 import ArticleDtoPricePerMarketType0  # noqa: PLC0415
        from ..models.article_nutriments_dto import ArticleNutrimentsDto  # noqa: PLC0415
        from ..models.auto_reduce_config_dto import AutoReduceConfigDto  # noqa: PLC0415
        from ..models.household_details_dto import HouseholdDetailsDto  # noqa: PLC0415
        from ..models.item_pantry_settings_dto import ItemPantrySettingsDto  # noqa: PLC0415
        from ..models.weighing_dto import WeighingDto  # noqa: PLC0415

        d = dict(src_dict)
        uuid = d.pop("uuid")

        name = d.pop("name")

        category_uuid = d.pop("categoryUuid")

        content_volume = d.pop("contentVolume")

        unit_id = d.pop("unitId")

        amount = d.pop("amount")

        manage_minimum_amount = d.pop("manageMinimumAmount")

        minimum_amount = d.pop("minimumAmount")

        minimum_amount_mode = MinimumAmountMode(d.pop("minimumAmountMode"))

        amount_to_buy = d.pop("amountToBuy")

        price_type = PriceType(d.pop("priceType"))

        discount_type = DiscountType(d.pop("discountType"))

        pantry_settings = ItemPantrySettingsDto.from_dict(d.pop("pantrySettings"))

        def _parse_brand(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        brand = _parse_brand(d.pop("brand", UNSET))

        def _parse_barcode(data: object) -> list[str] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                barcode_type_1 = cast(list[str], data)

                return barcode_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | str | Unset, data)

        barcode = _parse_barcode(d.pop("barcode", UNSET))

        def _parse_notes(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        notes = _parse_notes(d.pop("notes", UNSET))

        def _parse_supermarket_id(data: object) -> list[str] | None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                supermarket_id_type_1 = cast(list[str], data)

                return supermarket_id_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | str | Unset, data)

        supermarket_id = _parse_supermarket_id(d.pop("supermarketId", UNSET))

        def _parse_disable_min_amount(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        disable_min_amount = _parse_disable_min_amount(d.pop("disableMinAmount", UNSET))

        def _parse_merge_different_content(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        merge_different_content = _parse_merge_different_content(d.pop("mergeDifferentContent", UNSET))

        def _parse_placeholder_for_category_uuid(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        placeholder_for_category_uuid = _parse_placeholder_for_category_uuid(d.pop("placeholderForCategoryUuid", UNSET))

        def _parse_price(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        price = _parse_price(d.pop("price", UNSET))

        def _parse_deposit(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        deposit = _parse_deposit(d.pop("deposit", UNSET))

        def _parse_discount(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        discount = _parse_discount(d.pop("discount", UNSET))

        def _parse_discount_per_unit_or_total(data: object) -> None | PriceType | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                discount_per_unit_or_total_type_1 = PriceType(data)

                return discount_per_unit_or_total_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(None | PriceType | Unset, data)

        discount_per_unit_or_total = _parse_discount_per_unit_or_total(d.pop("discountPerUnitOrTotal", UNSET))

        def _parse_coupon_name(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        coupon_name = _parse_coupon_name(d.pop("couponName", UNSET))

        def _parse_coupon_expiration_date(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        coupon_expiration_date = _parse_coupon_expiration_date(d.pop("couponExpirationDate", UNSET))

        def _parse_image_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        image_url = _parse_image_url(d.pop("imageUrl", UNSET))

        def _parse_additional_image_urls(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                additional_image_urls_type_0 = cast(list[str], data)

                return additional_image_urls_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        additional_image_urls = _parse_additional_image_urls(d.pop("additionalImageUrls", UNSET))

        def _parse_predefined_pantry(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        predefined_pantry = _parse_predefined_pantry(d.pop("predefinedPantry", UNSET))

        def _parse_default_best_before_days(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        default_best_before_days = _parse_default_best_before_days(d.pop("defaultBestBeforeDays", UNSET))

        def _parse_purchase_date(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        purchase_date = _parse_purchase_date(d.pop("purchaseDate", UNSET))

        def _parse_last_inventory_date(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        last_inventory_date = _parse_last_inventory_date(d.pop("lastInventoryDate", UNSET))

        def _parse_last_modified(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        last_modified = _parse_last_modified(d.pop("lastModified", UNSET))

        def _parse_tags(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                tags_type_0 = cast(list[str], data)

                return tags_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        tags = _parse_tags(d.pop("tags", UNSET))

        def _parse_allergens(data: object) -> list[Allergen] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allergens_type_0 = []
                _allergens_type_0 = data
                for allergens_type_0_item_data in _allergens_type_0:
                    allergens_type_0_item = Allergen(allergens_type_0_item_data)

                    allergens_type_0.append(allergens_type_0_item)

                return allergens_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[Allergen] | None | Unset, data)

        allergens = _parse_allergens(d.pop("allergens", UNSET))

        def _parse_ingredient_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        ingredient_id = _parse_ingredient_id(d.pop("ingredientId", UNSET))

        _nutriments = d.pop("nutriments", UNSET)
        nutriments: ArticleNutrimentsDto | Unset
        if isinstance(_nutriments, Unset) or _nutriments is None:
            nutriments = UNSET
        else:
            nutriments = ArticleNutrimentsDto.from_dict(_nutriments)

        _household_details = d.pop("householdDetails", UNSET)
        household_details: HouseholdDetailsDto | Unset
        if isinstance(_household_details, Unset) or _household_details is None:
            household_details = UNSET
        else:
            household_details = HouseholdDetailsDto.from_dict(_household_details)

        _weighing = d.pop("weighing", UNSET)
        weighing: WeighingDto | Unset
        if isinstance(_weighing, Unset) or _weighing is None:
            weighing = UNSET
        else:
            weighing = WeighingDto.from_dict(_weighing)

        _complex_best_before_data = d.pop("complexBestBeforeData", UNSET)
        complex_best_before_data: ArticleCatalogBestBeforeDatesDto | Unset
        if isinstance(_complex_best_before_data, Unset) or _complex_best_before_data is None:
            complex_best_before_data = UNSET
        else:
            complex_best_before_data = ArticleCatalogBestBeforeDatesDto.from_dict(_complex_best_before_data)

        def _parse_generic_price_from_catalog(data: object) -> float | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(float | None | Unset, data)

        generic_price_from_catalog = _parse_generic_price_from_catalog(d.pop("genericPriceFromCatalog", UNSET))

        def _parse_price_per_market(data: object) -> ArticleDtoPricePerMarketType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                price_per_market_type_0 = ArticleDtoPricePerMarketType0.from_dict(data)

                return price_per_market_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ArticleDtoPricePerMarketType0 | None | Unset, data)

        price_per_market = _parse_price_per_market(d.pop("pricePerMarket", UNSET))

        list_id = d.pop("listId", UNSET)

        _auto_reduce = d.pop("autoReduce", UNSET)
        auto_reduce: AutoReduceConfigDto | Unset
        if isinstance(_auto_reduce, Unset) or _auto_reduce is None:
            auto_reduce = UNSET
        else:
            auto_reduce = AutoReduceConfigDto.from_dict(_auto_reduce)

        article_dto = cls(
            uuid=uuid,
            name=name,
            category_uuid=category_uuid,
            content_volume=content_volume,
            unit_id=unit_id,
            amount=amount,
            manage_minimum_amount=manage_minimum_amount,
            minimum_amount=minimum_amount,
            minimum_amount_mode=minimum_amount_mode,
            amount_to_buy=amount_to_buy,
            price_type=price_type,
            discount_type=discount_type,
            pantry_settings=pantry_settings,
            brand=brand,
            barcode=barcode,
            notes=notes,
            supermarket_id=supermarket_id,
            disable_min_amount=disable_min_amount,
            merge_different_content=merge_different_content,
            placeholder_for_category_uuid=placeholder_for_category_uuid,
            price=price,
            deposit=deposit,
            discount=discount,
            discount_per_unit_or_total=discount_per_unit_or_total,
            coupon_name=coupon_name,
            coupon_expiration_date=coupon_expiration_date,
            image_url=image_url,
            additional_image_urls=additional_image_urls,
            predefined_pantry=predefined_pantry,
            default_best_before_days=default_best_before_days,
            purchase_date=purchase_date,
            last_inventory_date=last_inventory_date,
            last_modified=last_modified,
            tags=tags,
            allergens=allergens,
            ingredient_id=ingredient_id,
            nutriments=nutriments,
            household_details=household_details,
            weighing=weighing,
            complex_best_before_data=complex_best_before_data,
            generic_price_from_catalog=generic_price_from_catalog,
            price_per_market=price_per_market,
            list_id=list_id,
            auto_reduce=auto_reduce,
        )

        article_dto.additional_properties = d
        return article_dto

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
