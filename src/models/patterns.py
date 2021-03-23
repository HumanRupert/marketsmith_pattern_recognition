from typing import Literal, List, Optional
from datetime import date

from pydantic import BaseModel, validator
from src.ms.utils import validate_n_parse_msdate

PatternType = Literal["consolidations",
                      "cupWithHandles", "doubleBottoms", "flatBases", "ascendingBases", "IPOs", "tightAreas"]


class PatternProperties(BaseModel):
    """Properties of a pattern (will be available in `properties` field of pattern object)"""
    Key: str
    Value: str


class CupWithHandle(BaseModel):
    """Represents a cup with handle pattern object passed by MarketSmith API"""
    baseID: int
    baseStartDate: date
    baseEndDate: date
    baseNumber: int
    baseStage: str
    baseStatus: int
    pivotPriceDate: date
    properties: List[PatternProperties]
    baseLength: int
    periodicity: int
    versionID: str
    leftSideHighDate: date
    patternType: int
    baseBottomDate: date
    firstBottomDate: date
    handleLowDate: date
    handleStartDate: date
    cupEndDate: date

    @validator("baseStartDate", "baseEndDate", "pivotPriceDate", "leftSideHighDate", "baseBottomDate", "firstBottomDate", "handleLowDate", "handleStartDate", "cupEndDate", pre=True, always=True)
    def validate_date(cls, v):
        return validate_n_parse_msdate(v)
