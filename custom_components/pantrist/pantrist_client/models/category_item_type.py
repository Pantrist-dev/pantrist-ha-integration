from enum import StrEnum


class CategoryItemType(StrEnum):
    FOOD = "food"
    NON_FOOD = "non-food"

    def __str__(self) -> str:
        return str(self.value)
