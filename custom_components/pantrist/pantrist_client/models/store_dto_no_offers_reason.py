from enum import StrEnum


class StoreDtoNoOffersReason(StrEnum):
    NO_SOURCE_FOR_REGION = "NO_SOURCE_FOR_REGION"

    def __str__(self) -> str:
        return str(self.value)
