import json
from typing import Literal, List

from pydantic import validate_arguments

from src.ms import AuthSession, get_instrument, get_user
from src.models import Instrument, User, PatternType, CupWithHandle
from src.ms.endpoints import GET_PATTERNS


@validate_arguments(config=dict(arbitrary_types_allowed=True))
def get_patterns(instrument: Instrument, user: User, session: AuthSession, start: int, end: int):
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
    cups: List[CupWithHandle] = patterns.get("cupWithHandles", None)
    if(cups == None):
        return

    cup_with_handles = [cup for cup in cups if cup["patternType"] == 1]
    return cup_with_handles