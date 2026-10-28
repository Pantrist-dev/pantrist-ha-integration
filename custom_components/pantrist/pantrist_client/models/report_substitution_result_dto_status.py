from enum import StrEnum


class ReportSubstitutionResultDtoStatus(StrEnum):
    DISABLED = "disabled"
    LIVE = "live"
    REJECTED = "rejected"

    def __str__(self) -> str:
        return str(self.value)
