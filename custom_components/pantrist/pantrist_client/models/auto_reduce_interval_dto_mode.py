from enum import StrEnum


class AutoReduceIntervalDtoMode(StrEnum):
    INTERVAL = "interval"

    def __str__(self) -> str:
        return str(self.value)
