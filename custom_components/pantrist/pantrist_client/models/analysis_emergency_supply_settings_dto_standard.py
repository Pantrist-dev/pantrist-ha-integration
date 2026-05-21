from enum import Enum


class AnalysisEmergencySupplySettingsDtoStandard(str, Enum):
    BMEL = "bmel"
    WFP = "wfp"

    def __str__(self) -> str:
        return str(self.value)
