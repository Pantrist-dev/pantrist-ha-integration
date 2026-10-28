from enum import StrEnum


class RecipeSubstitutableIngredientDtoKind(StrEnum):
    SUBSTITUTE = "substitute"
    VARIANT = "variant"

    def __str__(self) -> str:
        return str(self.value)
