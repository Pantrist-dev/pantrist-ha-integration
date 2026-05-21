from enum import Enum


class ApiFilterDtoSortBy(str, Enum):
    ALPHABETICALASC = "AlphabeticalAsc"
    ALPHABETICALDESC = "AlphabeticalDesc"
    FAVORITES = "Favorites"
    RANDOM = "Random"
    TOTALTIME = "TotalTime"

    def __str__(self) -> str:
        return str(self.value)
