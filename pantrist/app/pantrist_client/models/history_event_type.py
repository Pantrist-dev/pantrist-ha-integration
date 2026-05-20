from enum import Enum


class HistoryEventType(str, Enum):
    CREATED = "created"
    DELETED = "deleted"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
