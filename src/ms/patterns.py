import json
from typing import Literal, List
import csv
import time

from pydantic import validate_arguments, BaseModel

from src.ms import AuthSession, get_instrument, get_user
from src.models import Instrument, User, PatternType, CupWithHandle
from src.ms.endpoints import GET_PATTERNS


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def get_patterns(instrument: Instrument, user: User, session: AuthSession, start: int, end: int):
    """Gets all patterns for an instrument in a given period

    Parameters
    ----------
    instrument : Instrument
        Instrument object of the target name

    user : User
        Authenticated user

    session : AuthSession
        Authenticated session

    start : int
        Start in millis

    end : int
        End in millis

    Returns
    -------
    dict
        status of the response and the available patterns
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
            "endDate": end_date
        }
    }
    res = session.session.post(GET_PATTERNS, data=json.dumps(payload))
    res = res.json()
    return res


def flattern_pattern_properties(patterns: List[dict]) -> List[dict]:
    """Each received Pattern instance from MS includes a `properties` field, which is a list of dictionaries w/ the `Key` and `Value` fields and containts extra properties of the pattern. This method flattens Pattern instance by adding removing `properties` field and adding its keys as separate fields of instance.

    Parameters
    ----------
    patterns : List[dict]
        list of patterns fetched from MS

    Returns
    -------
    List[dict]
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
    patterns : object
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


def store_patterns(patterns: List[BaseModel], dataname: str, ticker: str):
    """Stores a given list of patterns to a `.csv` file in `data/patterns/` dir

    Parameters
    ----------
    patterns : List[BaseModel]
        list of pydantic models (records) of the patterns to be stored

    dataname : str
        prefix of the stored filename (current millis will be used as the second part of the filename to make filename unique)

    ticker : str
        ticker that the data belongs to, will be used in filename
    """
    # generate file name
    millis = round(time.time() * 1000)
    filepath = f"data/patterns/{ticker}_{dataname}_{millis}.csv"

    # convert to dict
    patterns = [pattern.dict() for pattern in patterns]
    keys = patterns[0].keys()

    with open(filepath, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(patterns)
