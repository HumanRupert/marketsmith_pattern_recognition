from typing import Union

from pydantic import BaseModel


class Constituent(BaseModel):
    """Represents a ticker received from FMP API when retrieving constituents of an index; see `price.load_tickers` method."""
    symbol: str
    name: str
    sector: str
    subSector: str
    headQuarter: Union[str, None]
    dateFirstAdded: str
    cik: Union[str, None]
    founded: Union[str, None]
