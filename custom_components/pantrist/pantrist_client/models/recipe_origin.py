from enum import StrEnum


class RecipeOrigin(StrEnum):
    COMMUNITY = "community"
    OFFERS = "offers"
    SOCIAL_IMPORT = "social_import"
    USER_CREATED = "user_created"
    WEB_IMPORT = "web_import"

    def __str__(self) -> str:
        return str(self.value)
