from enum import StrEnum


class ParseRecipeRequestDtoType(StrEnum):
    NORMAL = "normal"
    SMART = "smart"

    def __str__(self) -> str:
        return str(self.value)
