from enum import StrEnum


class SwipeDecisionDtoDecision(StrEnum):
    LIKE = "like"
    SKIP = "skip"

    def __str__(self) -> str:
        return str(self.value)
