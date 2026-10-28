from enum import StrEnum


class NutriScore(StrEnum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"

    def __str__(self) -> str:
        return str(self.value)
