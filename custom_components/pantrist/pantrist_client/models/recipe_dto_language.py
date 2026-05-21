from enum import Enum


class RecipeDtoLanguage(str, Enum):
    DE_DE = "de-DE"
    EN_GB = "en-GB"
    EN_US = "en-US"
    ES_ES = "es-ES"
    IT_IT = "it-IT"
    NL_NL = "nl-NL"
    PL_PL = "pl-PL"
    PT_BR = "pt-BR"
    PT_PT = "pt-PT"
    SV_SE = "sv-SE"

    def __str__(self) -> str:
        return str(self.value)
