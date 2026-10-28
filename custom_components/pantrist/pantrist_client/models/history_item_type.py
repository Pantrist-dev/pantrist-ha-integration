from enum import StrEnum


class HistoryItemType(StrEnum):
    INTERMEDIATE = "intermediate"
    PANTRY = "pantry"
    SHOPPING = "shopping"

    def __str__(self) -> str:
        return str(self.value)
