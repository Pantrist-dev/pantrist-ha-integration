from enum import StrEnum


class RecipeDeckRequestDtoExcludeAllergensItem(StrEnum):
    CELERY = "Celery"
    CRUSTACEANS = "Crustaceans"
    EGGS = "Eggs"
    FISH = "Fish"
    GLUTEN = "Gluten"
    LUPIN = "Lupin"
    MILK = "Milk"
    MOLLUSCS = "Molluscs"
    MUSTARD = "Mustard"
    NUTS = "Nuts"
    PEANUTS = "Peanuts"
    SESAME = "Sesame"
    SOYBEANS = "Soybeans"
    SULPHURDIOXIDE = "SulphurDioxide"

    def __str__(self) -> str:
        return str(self.value)
