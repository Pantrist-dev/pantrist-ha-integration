from enum import StrEnum


class UserDtoForcedPremiumTariff(StrEnum):
    FIVEUSERS = "fiveUsers"
    SINGLE = "single"
    TWOUSERS = "twoUsers"

    def __str__(self) -> str:
        return str(self.value)
