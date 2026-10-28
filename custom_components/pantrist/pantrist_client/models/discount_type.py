from enum import StrEnum


class DiscountType(StrEnum):
    CURRENCY = "currency"
    PERCENT = "percent"

    def __str__(self) -> str:
        return str(self.value)
