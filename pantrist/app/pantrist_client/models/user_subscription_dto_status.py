from enum import Enum


class UserSubscriptionDtoStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

    def __str__(self) -> str:
        return str(self.value)
