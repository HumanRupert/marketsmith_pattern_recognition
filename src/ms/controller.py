import src.ms as ms


def extract_patterns(ticker: str, filter_method: callable, start: int, end: int, session=None):
    if(session == None):
        session = ms.AuthSession()
    user = ms.get_user(session)
    instrument = ms.get_instrument(session, ticker)
    patterns = ms.get_patterns(instrument, user, session, start, end)
    filtered_patterns = filter_method(patterns)
    return filtered_patterns
