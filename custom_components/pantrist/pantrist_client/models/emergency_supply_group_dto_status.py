from enum import StrEnum


class EmergencySupplyGroupDtoStatus(StrEnum):
    CRITICAL = "critical"
    OK = "ok"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
