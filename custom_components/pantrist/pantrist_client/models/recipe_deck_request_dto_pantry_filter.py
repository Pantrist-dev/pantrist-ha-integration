from enum import StrEnum


class RecipeDeckRequestDtoPantryFilter(StrEnum):
    ALL = "all"
    EXPIRING = "expiring"

    def __str__(self) -> str:
        return str(self.value)
