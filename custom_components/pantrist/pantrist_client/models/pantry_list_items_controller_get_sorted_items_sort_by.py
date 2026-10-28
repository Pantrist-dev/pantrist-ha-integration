from enum import StrEnum


class PantryListItemsControllerGetSortedItemsSortBy(StrEnum):
    BESTBEFORE = "bestBefore"
    TIMESTAMP = "timestamp"

    def __str__(self) -> str:
        return str(self.value)
