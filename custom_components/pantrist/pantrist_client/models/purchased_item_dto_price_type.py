from enum import StrEnum


class PurchasedItemDtoPriceType(StrEnum):
    PERUNIT = "perUnit"
    PERVOLUME = "perVolume"
    PERWEIGHT = "perWeight"
    TOTAL = "total"

    def __str__(self) -> str:
        return str(self.value)
