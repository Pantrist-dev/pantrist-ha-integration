from enum import StrEnum


class Role(StrEnum):
    ADMIN = "Admin"
    OWNER = "Owner"
    USER = "User"

    def __str__(self) -> str:
        return str(self.value)
