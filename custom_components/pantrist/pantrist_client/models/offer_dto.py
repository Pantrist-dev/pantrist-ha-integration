from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.offer_dto_kind import OfferDtoKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.offer_ingredient_match_dto import OfferIngredientMatchDto


T = TypeVar("T", bound="OfferDto")


@_attrs_define
class OfferDto:
    """
    Attributes:
        id (str):
        title (str):
        valid_from (str): First day the offer is valid (ISO date). Lies in the future on a day between two leaflets
            (e.g. a Sunday for a Monday-to-Saturday chain): the market then shows the next leaflet, which starts within
            three days, so the client should label it as upcoming rather than current.
        valid_to (str): Last day the offer is valid (ISO date).
        ingredients (list[OfferIngredientMatchDto]): Catalog ingredients this offer was matched to. May be empty.
        brand (str | Unset):
        price_cents (float | Unset): Offer price in cents.
        ref_price_cents (float | Unset): Struck-through reference price in cents.
        unit_amount (float | Unset): Size of the whole pack, e.g. 1 with unitType "kg". For a multipack this is all
            units together: 10 (l) for a crate of 20 × 0,5 l, see packCount.
        unit_type (str | Unset):
        pack_count (float | Unset): How many equal units the pack holds, when more than one: 20 for a crate of 20 × 0,5
            l. One unit is unitAmount / packCount. Absent for a single unit or when the retailer does not say.
        kind (OfferDtoKind | Unset): clearance: sold until stock runs out; validTo is a rolling one-day window, not an
            end date. Prices are the chain's online prices.
        image_url (str | Unset): The retailer's own image URL. Load it directly from that URL — we neither store nor re-
            serve the image, and the retailer's server sees the request.
        source_category_slug (str | Unset): Stable machine key for the source's own department/category (e.g. "kaese-
            quark"), when it has one. Sparse — most offers have none. The app maps this to its own shopping-list category.
        source_category_name (str | Unset): Display name for sourceCategorySlug (e.g. "Käse").
        category_uuid (str | Unset): The app's own category id, already resolved from the source category. Pass this
            straight through when adding the offer to the shopping list; unset means the source had no (mappable) category,
            so the app's own name-based categorizer should decide instead.
    """

    id: str
    title: str
    valid_from: str
    valid_to: str
    ingredients: list[OfferIngredientMatchDto]
    brand: str | Unset = UNSET
    price_cents: float | Unset = UNSET
    ref_price_cents: float | Unset = UNSET
    unit_amount: float | Unset = UNSET
    unit_type: str | Unset = UNSET
    pack_count: float | Unset = UNSET
    kind: OfferDtoKind | Unset = UNSET
    image_url: str | Unset = UNSET
    source_category_slug: str | Unset = UNSET
    source_category_name: str | Unset = UNSET
    category_uuid: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        title = self.title

        valid_from = self.valid_from

        valid_to = self.valid_to

        ingredients = []
        for ingredients_item_data in self.ingredients:
            ingredients_item = ingredients_item_data.to_dict()
            ingredients.append(ingredients_item)

        brand = self.brand

        price_cents = self.price_cents

        ref_price_cents = self.ref_price_cents

        unit_amount = self.unit_amount

        unit_type = self.unit_type

        pack_count = self.pack_count

        kind: str | Unset = UNSET
        if not isinstance(self.kind, Unset):
            kind = self.kind.value

        image_url = self.image_url

        source_category_slug = self.source_category_slug

        source_category_name = self.source_category_name

        category_uuid = self.category_uuid

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "title": title,
                "validFrom": valid_from,
                "validTo": valid_to,
                "ingredients": ingredients,
            }
        )
        if brand is not UNSET:
            field_dict["brand"] = brand
        if price_cents is not UNSET:
            field_dict["priceCents"] = price_cents
        if ref_price_cents is not UNSET:
            field_dict["refPriceCents"] = ref_price_cents
        if unit_amount is not UNSET:
            field_dict["unitAmount"] = unit_amount
        if unit_type is not UNSET:
            field_dict["unitType"] = unit_type
        if pack_count is not UNSET:
            field_dict["packCount"] = pack_count
        if kind is not UNSET:
            field_dict["kind"] = kind
        if image_url is not UNSET:
            field_dict["imageUrl"] = image_url
        if source_category_slug is not UNSET:
            field_dict["sourceCategorySlug"] = source_category_slug
        if source_category_name is not UNSET:
            field_dict["sourceCategoryName"] = source_category_name
        if category_uuid is not UNSET:
            field_dict["categoryUuid"] = category_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.offer_ingredient_match_dto import OfferIngredientMatchDto  # noqa: PLC0415

        d = dict(src_dict)
        id = d.pop("id")

        title = d.pop("title")

        valid_from = d.pop("validFrom")

        valid_to = d.pop("validTo")

        ingredients = []
        _ingredients = d.pop("ingredients")
        for ingredients_item_data in _ingredients:
            ingredients_item = OfferIngredientMatchDto.from_dict(ingredients_item_data)

            ingredients.append(ingredients_item)

        brand = d.pop("brand", UNSET)

        price_cents = d.pop("priceCents", UNSET)

        ref_price_cents = d.pop("refPriceCents", UNSET)

        unit_amount = d.pop("unitAmount", UNSET)

        unit_type = d.pop("unitType", UNSET)

        pack_count = d.pop("packCount", UNSET)

        _kind = d.pop("kind", UNSET)
        kind: OfferDtoKind | Unset
        if isinstance(_kind, Unset) or _kind is None or _kind == "":
            kind = UNSET
        else:
            kind = OfferDtoKind(_kind)

        image_url = d.pop("imageUrl", UNSET)

        source_category_slug = d.pop("sourceCategorySlug", UNSET)

        source_category_name = d.pop("sourceCategoryName", UNSET)

        category_uuid = d.pop("categoryUuid", UNSET)

        offer_dto = cls(
            id=id,
            title=title,
            valid_from=valid_from,
            valid_to=valid_to,
            ingredients=ingredients,
            brand=brand,
            price_cents=price_cents,
            ref_price_cents=ref_price_cents,
            unit_amount=unit_amount,
            unit_type=unit_type,
            pack_count=pack_count,
            kind=kind,
            image_url=image_url,
            source_category_slug=source_category_slug,
            source_category_name=source_category_name,
            category_uuid=category_uuid,
        )

        offer_dto.additional_properties = d
        return offer_dto

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
