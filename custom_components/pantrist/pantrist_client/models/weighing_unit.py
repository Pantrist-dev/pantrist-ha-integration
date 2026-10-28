from enum import StrEnum


class WeighingUnit(StrEnum):
    G = "g"
    KG = "kg"
    LBS = "lbs"
    OZ = "oz"

    def __str__(self) -> str:
        return str(self.value)
