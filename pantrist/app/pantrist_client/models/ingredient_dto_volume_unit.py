from enum import Enum


class IngredientDtoVolumeUnit(str, Enum):
    FL_OZ = "fl-oz"
    G = "g"
    GAL = "gal"
    KG = "kg"
    L = "l"
    LBS = "lbs"
    ML = "ml"
    OZ = "oz"
    PACKET = "packet"
    PIECES = "pieces"
    PINCH = "Pinch"
    QT = "qt"
    TBSP = "tbsp"
    TSP = "tsp"

    def __str__(self) -> str:
        return str(self.value)
