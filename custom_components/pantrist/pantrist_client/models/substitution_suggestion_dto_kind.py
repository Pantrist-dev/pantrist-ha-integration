from enum import StrEnum


class SubstitutionSuggestionDtoKind(StrEnum):
    SUBSTITUTE = "substitute"
    VARIANT = "variant"

    def __str__(self) -> str:
        return str(self.value)
