from enum import StrEnum


class OfferIngredientMatchDtoMatchMethod(StrEnum):
    GTIN = "gtin"
    LLM = "llm"
    MANUAL = "manual"
    TEXT = "text"

    def __str__(self) -> str:
        return str(self.value)
