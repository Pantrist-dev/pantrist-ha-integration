from enum import StrEnum


class RecipeCollectionControllerGetCollectionsType(StrEnum):
    OWN = "own"
    SHARED = "shared"

    def __str__(self) -> str:
        return str(self.value)
