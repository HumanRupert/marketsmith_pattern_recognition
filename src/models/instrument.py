from datetime import date

from pydantic import BaseModel, validator


class Instrument(BaseModel):
    """Represents a financial `Instrument` object passed by MarketSmith API"""
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
        from src.ms.utils import convert_msdate_to_date
        return convert_msdate_to_date(v)
