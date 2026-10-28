from enum import StrEnum


class ValueWithMetricDtoMetric(StrEnum):
    DAYS = "days"
    MONTHS = "months"
    WEEKS = "weeks"
    YEARS = "years"

    def __str__(self) -> str:
        return str(self.value)
