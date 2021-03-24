from datetime import date


def convert_msdate_to_date(ms_date):
    """Converts date string passed by MarketSmith API to `date` object

    Parameters
    ----------
    ms_date : str
        e.g., "/Date(1536303600000-0700)/"

    Returns
    -------
    date
    """
    try:
        str_btwn_paranthesis = ms_date[ms_date.find("(")+1:ms_date.find(")")]

        if(str_btwn_paranthesis[0] == "-"):
            millis = int(str_btwn_paranthesis.split("-")[1]) * -1
        else:
            millis = int(str_btwn_paranthesis.split("-")[0])

        date_obj = date.fromtimestamp(millis/1000)
        return date_obj

    except TypeError:
        raise ValueError(
            "Invalid date received from MS. Must be like /Date(1536303600000-0700)/")
