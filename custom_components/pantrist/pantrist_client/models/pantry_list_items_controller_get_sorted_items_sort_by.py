from enum import Enum


class PantryListItemsControllerGetSortedItemsSortBy(str, Enum):
    BESTBEFORE = "bestBefore"
    TIMESTAMP = "timestamp"

    def __str__(self) -> str:
        return str(self.value)
