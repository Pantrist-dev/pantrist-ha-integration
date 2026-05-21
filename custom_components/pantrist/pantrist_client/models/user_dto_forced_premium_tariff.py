from enum import Enum


class UserDtoForcedPremiumTariff(str, Enum):
    FIVEUSERS = "fiveUsers"
    SINGLE = "single"
    TWOUSERS = "twoUsers"

    def __str__(self) -> str:
        return str(self.value)
