from enum import StrEnum


class AnalysisEmergencySupplySettingsDtoStandard(StrEnum):
    BMEL = "bmel"
    WFP = "wfp"

    def __str__(self) -> str:
        return str(self.value)
