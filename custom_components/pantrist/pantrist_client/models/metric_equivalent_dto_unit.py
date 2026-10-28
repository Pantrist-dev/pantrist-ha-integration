from enum import StrEnum


class MetricEquivalentDtoUnit(StrEnum):
    G = "g"
    ML = "ml"

    def __str__(self) -> str:
        return str(self.value)
