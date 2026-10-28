from enum import StrEnum


class UserSubscriptionDtoStore(StrEnum):
    APP_STORE = "APP_STORE"
    PLAY_STORE = "PLAY_STORE"
    STRIPE = "STRIPE"

    def __str__(self) -> str:
        return str(self.value)
