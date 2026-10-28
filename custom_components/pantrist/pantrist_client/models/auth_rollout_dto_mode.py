from enum import StrEnum


class AuthRolloutDtoMode(StrEnum):
    ALL = "all"
    ALLOWLIST = "allowlist"
    OFF = "off"
    PERCENT = "percent"

    def __str__(self) -> str:
        return str(self.value)
