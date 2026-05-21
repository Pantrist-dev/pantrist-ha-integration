from enum import Enum


class AccessTokenControllerAuthorizeCodeChallengeMethod(str, Enum):
    S256 = "S256"

    def __str__(self) -> str:
        return str(self.value)
