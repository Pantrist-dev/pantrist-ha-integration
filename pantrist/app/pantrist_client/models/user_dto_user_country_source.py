from enum import Enum


class UserDtoUserCountrySource(str, Enum):
    GEOLOCATION = "geolocation"
    IP = "ip"
    MANUALLY_SET = "manually-set"

    def __str__(self) -> str:
        return str(self.value)
