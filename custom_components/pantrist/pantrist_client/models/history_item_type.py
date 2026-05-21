from enum import Enum


class HistoryItemType(str, Enum):
    INTERMEDIATE = "intermediate"
    PANTRY = "pantry"
    SHOPPING = "shopping"

    def __str__(self) -> str:
        return str(self.value)
