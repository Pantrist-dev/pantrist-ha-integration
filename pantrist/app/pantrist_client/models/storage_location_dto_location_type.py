from enum import Enum


class StorageLocationDtoLocationType(str, Enum):
    FREEZER = "freezer"
    REFRIGERATOR = "refrigerator"
    UNREFRIGERATED = "unrefrigerated"

    def __str__(self) -> str:
        return str(self.value)
