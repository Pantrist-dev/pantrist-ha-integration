from enum import StrEnum


class AiRole(StrEnum):
    EXTRACTED = "extracted"
    GENERATED = "generated"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
