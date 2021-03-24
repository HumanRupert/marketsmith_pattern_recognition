from typing import Literal, List, Optional
from datetime import date

from pydantic import BaseModel, validator
from src.ms.utils import convert_msdate_to_date

PatternType = Literal["consolidations",
                      "cupWithHandles", "doubleBottoms", "flatBases", "ascendingBases", "IPOs", "tightAreas"]


class CupWithHandle(BaseModel):
    """Represents a cup with handle pattern object passed by MarketSmith API"""
    baseID: int
    baseStartDate: date
    baseEndDate: date
    baseNumber: int
    baseStage: str
    baseStatus: int
    pivotPriceDate: date
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
    UpBars: int
    BlueBars: int
    StallBars: int
    UpVolumeTotal: int
    DownBars: int
    RedBars: int
    SupportBars: int
    DownVolumeTotal: int
    BaseDepth: float
    AvgVolumeRatePctOnPivot: float
    VolumePctChangeOnPivot: float
    PricePctChangeOnPivot: float
    HandleDepth: float
    HandleLength: int
    CupLength: int

    @validator("baseStartDate", "baseEndDate", "pivotPriceDate", "leftSideHighDate", "baseBottomDate", "firstBottomDate", "handleLowDate", "handleStartDate", "cupEndDate", pre=True, always=True)
    def validate_date(cls, v):
        return convert_msdate_to_date(v)
