from enum import StrEnum


class ListWeekPlanControllerRemoveEntryType(StrEnum):
    MANUAL = "manual"
    RECIPE = "recipe"

    def __str__(self) -> str:
        return str(self.value)
