from enum import StrEnum


class ValueWithMetricAndOpeningDtoMetric(StrEnum):
    DAYS = "days"
    MONTHS = "months"
    WEEKS = "weeks"
    YEARS = "years"

    def __str__(self) -> str:
        return str(self.value)
