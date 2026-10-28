from enum import StrEnum


class AutoReduceWeekdayDtoMode(StrEnum):
    WEEKDAY = "weekday"

    def __str__(self) -> str:
        return str(self.value)
