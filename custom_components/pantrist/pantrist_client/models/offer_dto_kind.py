from enum import StrEnum


class OfferDtoKind(StrEnum):
    CLEARANCE = "clearance"

    def __str__(self) -> str:
        return str(self.value)
