from enum import StrEnum


class WeekPlanReceiptDtoType(StrEnum):
    MANUAL = "manual"
    RECIPE = "recipe"

    def __str__(self) -> str:
        return str(self.value)
