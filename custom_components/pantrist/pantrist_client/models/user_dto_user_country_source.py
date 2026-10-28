from enum import StrEnum


class UserDtoUserCountrySource(StrEnum):
    GEOLOCATION = "geolocation"
    IP = "ip"
    MANUALLY_SET = "manually-set"

    def __str__(self) -> str:
        return str(self.value)
