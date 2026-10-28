from enum import StrEnum


class MinimumAmountMode(StrEnum):
    CONTENT = "content"
    PACKAGES = "packages"

    def __str__(self) -> str:
        return str(self.value)
