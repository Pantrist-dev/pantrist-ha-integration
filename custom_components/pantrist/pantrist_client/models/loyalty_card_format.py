from enum import StrEnum


class LoyaltyCardFormat(StrEnum):
    AZTEC = "aztec"
    CODABAR = "codabar"
    CODE128 = "code128"
    CODE39 = "code39"
    CODE93 = "code93"
    DATAMATRIX = "datamatrix"
    EAN13 = "ean13"
    EAN8 = "ean8"
    ITF = "itf"
    PDF417 = "pdf417"
    QR = "qr"
    UPCA = "upca"
    UPCE = "upce"

    def __str__(self) -> str:
        return str(self.value)
