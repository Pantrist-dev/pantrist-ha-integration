from enum import StrEnum


class OfferIngredientMatchDtoDiet(StrEnum):
    FISH = "fish"
    MEAT = "meat"
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"

    def __str__(self) -> str:
        return str(self.value)
