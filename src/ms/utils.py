from datetime import date, datetime
import logging
import csv
from typing import List

from pydantic import BaseModel

from src.constants import DATE_FORMAT


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


def convert_defdate_to_datetime(default_date: str) -> datetime:
    """Converts a date string w/ default format defined in `constants.DATE_FORMAT` to a `datetime` object

    Parameters
    ----------
    default_date : `str`
        default date string

    Returns
    -------
    `datetime`
    """
    try:
        return datetime.strptime(default_date, DATE_FORMAT)
    except (ValueError, TypeError) as e:
        logging.error(
            "Invalid datetime format passed to convert_defdate_to_date.")
        raise


def convert_defdate_to_timestamp(default_date: str) -> int:
    """Converts a date string w/ default format defined in `constants.DATE_FORMAT` to a timestamp

    Parameters
    ----------
    default_date : `str`
        default date string

    Returns
    -------
    `int`
    """
    datetime_obj = convert_defdate_to_datetime(default_date)
    return datetime_obj.timestamp() * 1000


def convert_csv_to_records(filepath: str, klass: BaseModel) -> List[BaseModel]:
    """Converts a CSV file to a list of models

    Parameters
    ----------
    filepath : `str`
        filepath of CSV file

    klass : `BaseModel`
        pydantic model to use for serializing the CSV records

    Returns
    -------
    `List[BaseModel]`
        serialized CSV records
    """
    with open(filepath) as f:
        records = [
            klass(**{k: v for k, v in row.items()})
            for row in csv.DictReader(f, skipinitialspace=True)]
        return records
