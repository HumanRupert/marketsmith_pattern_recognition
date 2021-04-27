from pydantic import BaseModel


class Constituent(BaseModel):
    """Represents a ticker received from FMP API when retrieving constituents of an index; see `price.load_djia_constituents` method."""
    symbol: str
    name: str
    sector: str
    subSector: str
    headQuarter: str
    dateFirstAdded: str
    cik: str
    founded: str
