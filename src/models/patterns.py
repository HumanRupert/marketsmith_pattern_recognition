from typing import Literal, List

from pydantic import BaseModel

PatternType = Literal["consolidations",
                      "cupWithHandles", "doubleBottoms", "flatBases", "ascendingBases", "IPOs", "tightAreas"]


class PatternProperties(BaseModel):
    Key: str
    Value: str


class CupWithHandle(BaseModel):
    baseID: int
    baseStartDate: str
    baseEndDate: str
    baseNumber: int
    baseStage: str
    baseStatus: int
    pivotDate: str
    pivotPriceDate: str
    properties: List[PatternProperties]
    baseLength: int
    periodicity: int
    versionID: str
    leftSideHighDate: str
    patternType: int
    baseBottomDate: str
    firstBottomDate: str
    handleLowDate: str
    handleStartDate: str
    cupEndDate: str
