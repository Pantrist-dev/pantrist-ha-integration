from enum import StrEnum


class AppVersionPolicyDtoPlatform(StrEnum):
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"

    def __str__(self) -> str:
        return str(self.value)
