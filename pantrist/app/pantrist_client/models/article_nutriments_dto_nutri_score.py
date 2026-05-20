from enum import Enum


class ArticleNutrimentsDtoNutriScore(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"

    def __str__(self) -> str:
        return str(self.value)
