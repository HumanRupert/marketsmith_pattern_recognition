from pydantic import BaseModel


class Instrument(BaseModel):
    mSID: int
    type: int
    instrumentID: int
    symbol: str
    name: str
    earliestTradingDate: str
    latestTradingDate: str
    hasComponents: bool
    hasOptions: bool
    isActive: bool
