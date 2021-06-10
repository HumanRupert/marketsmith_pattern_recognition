import json
from typing import Literal, List
import csv

from pydantic import validate_arguments, BaseModel

from src.ms import AuthSession, get_instrument, get_user
from src.models import Instrument, User, CupWithHandle
from src.ms.endpoints import GET_PATTERNS


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def get_patterns(instrument: Instrument, user: User, session: AuthSession, start: int, end: int) -> dict:
    """Gets all patterns for an instrument in a given period

    Parameters
    ----------
    instrument : `Instrument`
        Instrument object of the target name

    user : `User`
        Authenticated user

    session : `AuthSession`
        Authenticated session

    start : `int`
        Start in millis

    end : `int`
        End in millis

    Returns
    -------
    `dict`
    """
    start_date = f"/Date({start})/"
    end_date = f"/Date({end})/"
    payload = {
        "userID": user.UserID,
        "symbol": instrument.symbol,
        "instrumentID": instrument.instrumentID,
        "instrumentType": instrument.type,
        "dateInfo": {
            "startDate": start_date,
            "endDate": end_date,
            "frequency": 1,
            "tickCount": 0
        }
    }
    res = session.session.post(GET_PATTERNS, json=payload)
    res = res.json()
    return res


def flattern_pattern_properties(patterns: List[dict]) -> List[dict]:
    """Each received Pattern instance from MS includes a `properties` field, which is a list of dictionaries w/ the `Key` and `Value` fields and containts extra properties of the pattern. This method flattens Pattern instance by adding removing `properties` field and adding its keys as separate fields of instance.

    Parameters
    ----------
    patterns : `List[dict]`
        list of patterns fetched from MS

    Returns
    -------
    `List[dict]`
        flattened patterns
    """
    # add properties field as separate keys
    pattern_properties = [pattern.pop("properties", None)
                          for pattern in patterns]
    for index, props in enumerate(pattern_properties):
        for prop in props:
            patterns[index][prop["Key"]] = prop["Value"]

    return patterns


def filter_cup_with_handles(patterns) -> List[CupWithHandle]:
    """Given the response object of `GET_PATTERNS` endpoint, filters cup with handle patterns from it

    Parameters
    ----------
    patterns : `object`
        response of `GET_PATTERNS` endpoint

    Returns
    -------
    List[CupWithHandle]
        list of cup with handles patterns
    """
    # cups w/ or w/o a handle
    cups: List[CupWithHandle] = patterns.get("cupWithHandles", None)
    if(cups == None):
        return

    # cups w/ handle
    cup_with_handles = [cup
                        for cup in cups
                        if cup["patternType"] == 1]
    cup_with_handles = flattern_pattern_properties(cup_with_handles)
    cup_with_handles = [CupWithHandle(**cup) for cup in cup_with_handles]

    return cup_with_handles


def store_patterns(patterns: List[BaseModel], ticker: str) -> None:
    """Stores a given list of patterns to `data/patterns.csv`

    Parameters
    ----------
    patterns : `List[BaseModel]`
        list of pydantic models (records) of the patterns to be stored

    ticker : `str`
        ticker that the data belongs to
    """
    filepath = "data/patterns.csv"

    # convert to dict
    patterns = [{**pattern.dict(), "symbol": ticker}for pattern in patterns]
    keys = patterns[0].keys()

    # check if is empty
    with open(filepath, "r") as patterns_file:
        csv_dict = [row for row in csv.DictReader(patterns_file)]
        is_empty = len(csv_dict) == 0

    with open(filepath, 'a') as patterns_file:
        dict_writer = csv.DictWriter(patterns_file, keys)
        is_empty and dict_writer.writeheader()
        dict_writer.writerows(patterns)
