from enum import StrEnum


class PriceType(StrEnum):
    PERUNIT = "perUnit"
    TOTAL = "total"

    def __str__(self) -> str:
        return str(self.value)
