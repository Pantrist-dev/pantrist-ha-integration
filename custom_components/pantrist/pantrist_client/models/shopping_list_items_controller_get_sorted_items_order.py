from enum import StrEnum


class ShoppingListItemsControllerGetSortedItemsOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"

    def __str__(self) -> str:
        return str(self.value)
