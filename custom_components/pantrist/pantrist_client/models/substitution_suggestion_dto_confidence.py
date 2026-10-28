from enum import StrEnum


class SubstitutionSuggestionDtoConfidence(StrEnum):
    EMERGENCY = "emergency"
    GOOD = "good"
    PERFECT = "perfect"

    def __str__(self) -> str:
        return str(self.value)
