from datetime import datetime
import logging
from typing import List

import src.ms as ms
from src.ms.utils import convert_csv_to_records
from src.models import Constituent
from src.ms.pattern import filter_cup_with_handles

logging.basicConfig(level=logging.INFO)


def extract_patterns(ticker: str, filter_method: callable, start: int, end: int, session=ms.AuthSession()) -> list:
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


def extract_n_store_patterns(ticker: str, filter_method: callable, start: int, end: int,  dataname: str, session=ms.AuthSession()) -> None:
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
         name to use for storing data

    session : `AuthSession`, optional
        authenticated session, by default `ms.AuthSession()`
    """
    # load and extract patterns
    patterns = extract_patterns(ticker, filter_method, start, end)

    # n' store them
    ms.store_patterns(patterns, dataname, ticker)


def extract_n_store_cup_with_handles(start: int, end: int, tickers: List[Constituent]) -> None:
    """Loads tickers from `data/tickers.csv`, calls `extract_patterns` for each ticker to load Cup With Handle patterns, and then stores them in `data/patterns/ as CSV files

    Parameters
    ----------
    start : `int`
        start date in millis

    end : `int`
        end date in millis
    """
    for ix, ticker in enumerate(tickers):
        logging.info(f"Fetching data for {ticker.symbol}")
        logging.info(f"{ix}/{len(tickers)}")
        patterns = extract_patterns(
            ticker=ticker.symbol, filter_method=filter_cup_with_handles, start=start, end=end)
        ms.store_patterns(patterns=patterns, ticker=ticker.symbol)

        logging.info("––––––––––––––")


if __name__ == "__main__":
    tickers: List[Constituent] = convert_csv_to_records(
        "data/tickers.csv", Constituent)
    extract_n_store_cup_with_handles(1304411415000, 1619739000000, tickers)
