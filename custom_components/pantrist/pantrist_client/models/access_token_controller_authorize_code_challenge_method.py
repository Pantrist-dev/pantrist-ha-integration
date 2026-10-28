from enum import StrEnum


class AccessTokenControllerAuthorizeCodeChallengeMethod(StrEnum):
    S256 = "S256"

    def __str__(self) -> str:
        return str(self.value)
