from enum import Enum


class ShoppingListItemsControllerGetSortedItemsOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

    def __str__(self) -> str:
        return str(self.value)
