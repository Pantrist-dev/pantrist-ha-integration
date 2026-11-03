from enum import StrEnum


class EmergencySupplyGroupDtoUnit(StrEnum):
    KG = "kg"
    L = "l"

    def __str__(self) -> str:
        return str(self.value)
