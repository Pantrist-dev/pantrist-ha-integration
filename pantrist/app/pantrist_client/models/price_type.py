from enum import Enum


class PriceType(str, Enum):
    PERUNIT = "perUnit"
    TOTAL = "total"

    def __str__(self) -> str:
        return str(self.value)
