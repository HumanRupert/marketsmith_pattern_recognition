import json
from typing import Literal, List

from pydantic import validate_arguments

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
    cup_with_handles = [CupWithHandle(**cup)
                        for cup in cups
                        if cup["patternType"] == 1]
    return cup_with_handles
