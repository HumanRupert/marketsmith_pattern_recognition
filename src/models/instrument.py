from datetime import date

from pydantic import BaseModel, validator

from src.ms.utils import convert_msdate_to_date


class Instrument(BaseModel):
    """Represents a financial instrument object passed by MarketSmith API"""
    mSID: int
    type: int
    instrumentID: int
    symbol: str
    name: str
    earliestTradingDate: date
    latestTradingDate: date
    hasComponents: bool
    hasOptions: bool
    isActive: bool

    @validator("earliestTradingDate", "latestTradingDate", pre=True, always=True)
    def validate_date(cls, v):
        return convert_msdate_to_date(v)
