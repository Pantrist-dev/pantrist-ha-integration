from enum import StrEnum


class ChangeAmountOfItemDtoSource(StrEnum):
    AUTO_REDUCE = "auto_reduce"
    BARCODE = "barcode"
    MANUAL = "manual"
    NFC = "nfc"
    RESTOCK = "restock"
    SET_AMOUNT = "set_amount"
    SHORTCUT = "shortcut"

    def __str__(self) -> str:
        return str(self.value)
