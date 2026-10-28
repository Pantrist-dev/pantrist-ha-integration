from enum import StrEnum


class BuyReminderRowDtoConfidence(StrEnum):
    HIGH = "high"
    LOW = "low"

    def __str__(self) -> str:
        return str(self.value)
