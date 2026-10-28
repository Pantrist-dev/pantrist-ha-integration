from enum import StrEnum


class ApiFilterDtoPantryFilter(StrEnum):
    ALL = "all"
    EXPIRING = "expiring"

    def __str__(self) -> str:
        return str(self.value)
