from enum import Enum


class DiscountType(str, Enum):
    CURRENCY = "currency"
    PERCENT = "percent"

    def __str__(self) -> str:
        return str(self.value)
