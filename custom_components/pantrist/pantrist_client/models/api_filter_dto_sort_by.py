from enum import StrEnum


class ApiFilterDtoSortBy(StrEnum):
    ALPHABETICALASC = "AlphabeticalAsc"
    ALPHABETICALDESC = "AlphabeticalDesc"
    FAVORITES = "Favorites"
    NEWEST = "Newest"
    RANDOM = "Random"
    TOTALTIME = "TotalTime"

    def __str__(self) -> str:
        return str(self.value)
