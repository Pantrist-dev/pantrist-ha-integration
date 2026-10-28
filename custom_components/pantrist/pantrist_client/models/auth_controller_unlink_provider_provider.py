from enum import StrEnum


class AuthControllerUnlinkProviderProvider(StrEnum):
    APPLE_COM = "apple.com"
    FACEBOOK_COM = "facebook.com"
    GOOGLE_COM = "google.com"

    def __str__(self) -> str:
        return str(self.value)
