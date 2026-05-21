from enum import Enum


class PurchasedItemDtoPriceType(str, Enum):
    PERUNIT = "perUnit"
    PERVOLUME = "perVolume"
    PERWEIGHT = "perWeight"
    TOTAL = "total"

    def __str__(self) -> str:
        return str(self.value)
