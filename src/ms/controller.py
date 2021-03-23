import src.ms as ms


def extract_patterns(ticker: str, filter_method: callable, start: int, end: int, session=ms.AuthSession()):
    """Extracts a set of patterns, given a filter method, from MarketSmith API

    Parameters
    ----------
    ticker : str
        symbol of Instrument to get the data for

    filter_method : callable
        method that filters target patterns from `GET_PATTERNS` endpoint response

    start : int
        start date in millis

    end : int
        end date in millis

    session : AuthSession, optional
        authenticated session, by default ms.AuthSession()

    Returns
    -------
    List
        List of filtered patterns
    """
    user = ms.get_user(session)
    instrument = ms.get_instrument(session, ticker)
    patterns = ms.get_patterns(instrument, user, session, start, end)
    filtered_patterns = filter_method(patterns)
    return filtered_patterns
