from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="OfferRecipeIngredientDto")


@_attrs_define
class OfferRecipeIngredientDto:
    """
    Attributes:
        name (str): Ingredient name as it appears in the recipe.
        amount (float): Amount the recipe calls for.
        unit (str): Unit the recipe states the amount in.
        in_offer (bool): False when no current offer covers this ingredient. Such an ingredient carries no price at all
            rather than an invented one.
        cost_is_upper_bound (bool): True when the share above is an upper bound rather than a proportion, because no
            pack size was published or the recipe states an amount like "2 pieces" that does not convert into one. Render it
            as "at most", never as a price.
        offer_id (str | Unset): The offer this was priced from.
        offer_title (str | Unset): Offer headline, as the leaflet prints it.
        offer_image_url (str | Unset): The leaflet's own picture of the offer, where the source published one. What the
            shelf looks like settles in one glance whether the match is the right product, which a headline often does not.
        offer_brand (str | Unset): Brand the leaflet names, where it names one. Together with the picture it is what
            tells a shopper whether this is the product they meant.
        offer_substitutes_for (str | Unset): Set when the offer is not the ingredient itself but something that may
            stand in for it, because the ingredient is off the caller's diet: a vegan reading a Frikadellen recipe is shown
            the plant-based mince that is on offer, not the beef. Carries the recipe ingredient's own name, so the page can
            say what is being replaced. Example: Hackfleisch.
        offer_substitution_note (str | Unset): Why that swap is acceptable, from the curated substitution edge, in the
            requested language. Example: Pflanzliche Variante, 1:1 ersetzbar.
        store_name (str | Unset): Store the offer is at.
        retailer_key (str | Unset): Retailer key of that store.
        valid_from (str | Unset): First day this offer is valid (ISO date).
        valid_to (str | Unset): Last day this offer is valid (ISO date).
        offer_price_cents (float | Unset): Offer price for the whole pack, in cents.
        ref_price_cents (float | Unset): The struck-through reference price in cents, where the chain publishes one.
        estimated_cost_cents (float | Unset): Share of the pack price attributable to the amount this recipe uses, in
            cents.
    """

    name: str
    amount: float
    unit: str
    in_offer: bool
    cost_is_upper_bound: bool
    offer_id: str | Unset = UNSET
    offer_title: str | Unset = UNSET
    offer_image_url: str | Unset = UNSET
    offer_brand: str | Unset = UNSET
    offer_substitutes_for: str | Unset = UNSET
    offer_substitution_note: str | Unset = UNSET
    store_name: str | Unset = UNSET
    retailer_key: str | Unset = UNSET
    valid_from: str | Unset = UNSET
    valid_to: str | Unset = UNSET
    offer_price_cents: float | Unset = UNSET
    ref_price_cents: float | Unset = UNSET
    estimated_cost_cents: float | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        amount = self.amount

        unit = self.unit

        in_offer = self.in_offer

        cost_is_upper_bound = self.cost_is_upper_bound

        offer_id = self.offer_id

        offer_title = self.offer_title

        offer_image_url = self.offer_image_url

        offer_brand = self.offer_brand

        offer_substitutes_for = self.offer_substitutes_for

        offer_substitution_note = self.offer_substitution_note

        store_name = self.store_name

        retailer_key = self.retailer_key

        valid_from = self.valid_from

        valid_to = self.valid_to

        offer_price_cents = self.offer_price_cents

        ref_price_cents = self.ref_price_cents

        estimated_cost_cents = self.estimated_cost_cents

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "amount": amount,
                "unit": unit,
                "inOffer": in_offer,
                "costIsUpperBound": cost_is_upper_bound,
            }
        )
        if offer_id is not UNSET:
            field_dict["offerId"] = offer_id
        if offer_title is not UNSET:
            field_dict["offerTitle"] = offer_title
        if offer_image_url is not UNSET:
            field_dict["offerImageUrl"] = offer_image_url
        if offer_brand is not UNSET:
            field_dict["offerBrand"] = offer_brand
        if offer_substitutes_for is not UNSET:
            field_dict["offerSubstitutesFor"] = offer_substitutes_for
        if offer_substitution_note is not UNSET:
            field_dict["offerSubstitutionNote"] = offer_substitution_note
        if store_name is not UNSET:
            field_dict["storeName"] = store_name
        if retailer_key is not UNSET:
            field_dict["retailerKey"] = retailer_key
        if valid_from is not UNSET:
            field_dict["validFrom"] = valid_from
        if valid_to is not UNSET:
            field_dict["validTo"] = valid_to
        if offer_price_cents is not UNSET:
            field_dict["offerPriceCents"] = offer_price_cents
        if ref_price_cents is not UNSET:
            field_dict["refPriceCents"] = ref_price_cents
        if estimated_cost_cents is not UNSET:
            field_dict["estimatedCostCents"] = estimated_cost_cents

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        amount = d.pop("amount")

        unit = d.pop("unit")

        in_offer = d.pop("inOffer")

        cost_is_upper_bound = d.pop("costIsUpperBound")

        offer_id = d.pop("offerId", UNSET)

        offer_title = d.pop("offerTitle", UNSET)

        offer_image_url = d.pop("offerImageUrl", UNSET)

        offer_brand = d.pop("offerBrand", UNSET)

        offer_substitutes_for = d.pop("offerSubstitutesFor", UNSET)

        offer_substitution_note = d.pop("offerSubstitutionNote", UNSET)

        store_name = d.pop("storeName", UNSET)

        retailer_key = d.pop("retailerKey", UNSET)

        valid_from = d.pop("validFrom", UNSET)

        valid_to = d.pop("validTo", UNSET)

        offer_price_cents = d.pop("offerPriceCents", UNSET)

        ref_price_cents = d.pop("refPriceCents", UNSET)

        estimated_cost_cents = d.pop("estimatedCostCents", UNSET)

        offer_recipe_ingredient_dto = cls(
            name=name,
            amount=amount,
            unit=unit,
            in_offer=in_offer,
            cost_is_upper_bound=cost_is_upper_bound,
            offer_id=offer_id,
            offer_title=offer_title,
            offer_image_url=offer_image_url,
            offer_brand=offer_brand,
            offer_substitutes_for=offer_substitutes_for,
            offer_substitution_note=offer_substitution_note,
            store_name=store_name,
            retailer_key=retailer_key,
            valid_from=valid_from,
            valid_to=valid_to,
            offer_price_cents=offer_price_cents,
            ref_price_cents=ref_price_cents,
            estimated_cost_cents=estimated_cost_cents,
        )

        offer_recipe_ingredient_dto.additional_properties = d
        return offer_recipe_ingredient_dto

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
