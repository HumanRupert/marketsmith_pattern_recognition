from typing import Literal, List, Optional
from datetime import date

from pydantic import BaseModel, validator


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

    @validator("baseStartDate", "baseEndDate", "pivotPriceDate", "leftSideHighDate", "firstBottomDate", "handleLowDate", "handleStartDate", "cupEndDate", pre=True, always=True)
    def validate_date(cls, v):
        from src.ms.utils import convert_msdate_to_date
        return convert_msdate_to_date(v)
