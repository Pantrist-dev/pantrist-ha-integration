from enum import Enum


class PublicUserDtoForcedPremiumTariff(str, Enum):
    FIVEUSERS = "fiveUsers"
    SINGLE = "single"
    TWOUSERS = "twoUsers"

    def __str__(self) -> str:
        return str(self.value)
