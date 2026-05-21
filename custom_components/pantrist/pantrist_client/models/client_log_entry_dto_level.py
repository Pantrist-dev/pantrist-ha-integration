from enum import Enum


class ClientLogEntryDtoLevel(str, Enum):
    ERROR = "error"
    INFO = "info"
    WARN = "warn"

    def __str__(self) -> str:
        return str(self.value)
