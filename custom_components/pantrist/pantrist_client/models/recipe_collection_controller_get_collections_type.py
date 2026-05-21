from enum import Enum


class RecipeCollectionControllerGetCollectionsType(str, Enum):
    OWN = "own"
    SHARED = "shared"

    def __str__(self) -> str:
        return str(self.value)
