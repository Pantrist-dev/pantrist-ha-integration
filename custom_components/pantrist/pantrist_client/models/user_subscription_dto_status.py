from enum import StrEnum


class UserSubscriptionDtoStatus(StrEnum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

    def __str__(self) -> str:
        return str(self.value)
