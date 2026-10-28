from enum import StrEnum


class MarketArrivalTransitionDtoTransition(StrEnum):
    ENTER = "enter"
    EXIT = "exit"

    def __str__(self) -> str:
        return str(self.value)
