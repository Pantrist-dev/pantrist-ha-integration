from enum import StrEnum


class LocationType(StrEnum):
    FREEZER = "freezer"
    REFRIGERATOR = "refrigerator"
    UNREFRIGERATED = "unrefrigerated"

    def __str__(self) -> str:
        return str(self.value)
