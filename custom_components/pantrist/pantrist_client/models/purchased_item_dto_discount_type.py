from enum import StrEnum


class PurchasedItemDtoDiscountType(StrEnum):
    CURRENCY = "currency"
    NONE = "none"
    PERCENT = "percent"

    def __str__(self) -> str:
        return str(self.value)
