from datetime import datetime

import src.ms as ms
from src.constants import TICKER, DATE_FORMAT
from src.ms.utils import convert_defdate_to_timestamp


def extract_patterns(ticker: str, filter_method: callable, start: int, end: int, session=ms.AuthSession()):
    """Extracts a set of patterns, given a filter method, from MarketSmith API

    Parameters
    ----------
    ticker : `str`
        symbol of Instrument to get the data for

    filter_method : callable
        method that filters target patterns from `GET_PATTERNS` endpoint response

    start : `int`
        start date in millis

    end : `int`
        end date in millis

    session : `AuthSession`, optional
        authenticated session, by default ms.AuthSession()

    Returns
    -------
    `list`
        List of filtered patterns
    """
    user = ms.get_user(session)
    instrument = ms.get_instrument(session, ticker)
    patterns = ms.get_patterns(instrument, user, session, start, end)
    filtered_patterns = filter_method(patterns)
    return filtered_patterns


def extract_n_store_patterns(ticker: str, filter_method: callable, start: str, end: str,  dataname: str, session=ms.AuthSession()):
    """Extracts patterns from MS API and stores them in `data/` dir

    Parameters
    ----------
    ticker : `str`
        symbol of Instrument to get the data for

    filter_method : `callable`
        method that filters target patterns from `GET_PATTERNS` endpoint response

    start : `int`
        start date in millis

    end : `int`
        end date in millis

    dataname : `str`
         name to use for storing t data

    session : `AuthSession`, optional
        authenticated session, by default ms.AuthSession()
    """
    # convert datr strings to millis
    start, end = convert_defdate_to_timestamp(
        start), convert_defdate_to_timestamp(end)
    # load and extract patterns
    patterns = extract_patterns(ticker, filter_method, start, end)
    # n' store them
    ms.store_patterns(patterns, dataname, ticker)
