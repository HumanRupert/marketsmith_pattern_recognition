import logging

from pydantic import validate_arguments

from src.ms import AuthSession
from src.ms.endpoints import SEARCH_INSTRUMENTS
from src.models import Instrument


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def get_instrument(session: AuthSession, symbol: str):
    """Given a symbol (ticker), gets the corresponding Instrument from MarketSmith API

    Parameters
    ----------
    session : AuthSession
        authenticated session

    symbol : str
        ticker of Instrument

    Raises
    ----------
    AssertionError
        if the length of search results for the ticker is more than one

    Returns
    -------
    Instrument
    """
    # search in instruments
    data = f"\"{symbol}\""
    search_results = session.session.post(
        SEARCH_INSTRUMENTS, data=data)
    search_results = search_results.json()["content"]

    # in search results, find the exact match
    instrument = list(filter(
        lambda result: result['symbol'] == symbol, search_results))

    # there shouldn't be less or more than 1 exact match
    try:
        assert len(instrument) == 1
    except AssertionError:
        logging.error(
            f"Only 1 exact match should be found. Found {len(instrument)}")
        raise

    instrument = Instrument(**instrument[0])
    return instrument
