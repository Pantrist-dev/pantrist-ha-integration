from enum import Enum


class PurchasedItemDtoDiscountType(str, Enum):
    CURRENCY = "currency"
    NONE = "none"
    PERCENT = "percent"

    def __str__(self) -> str:
        return str(self.value)
