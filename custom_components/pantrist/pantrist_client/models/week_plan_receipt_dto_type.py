from enum import Enum


class WeekPlanReceiptDtoType(str, Enum):
    MANUAL = "manual"
    RECIPE = "recipe"

    def __str__(self) -> str:
        return str(self.value)
