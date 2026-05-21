from enum import Enum


class ParseRecipeRequestDtoType(str, Enum):
    NORMAL = "normal"
    SMART = "smart"

    def __str__(self) -> str:
        return str(self.value)
