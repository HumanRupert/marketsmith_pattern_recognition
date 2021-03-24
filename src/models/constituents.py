from pydantic import BaseModel


class Constituent(BaseModel):
    """Represents an index constituent fetched from FMP API"""
    symbol: str
    name: str
    sector: str
    subSector: str
    headQuarter: str
    dateFirstAdded: str
    cik: str
    founded: str
