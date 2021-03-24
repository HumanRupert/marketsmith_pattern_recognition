import os
import csv
from typing import List

import requests
from dotenv import load_dotenv
from pydantic import parse_obj_as

from src.constants import DJIA_CONSTITUENTS_URL
from src.models import Constituent

load_dotenv()


def load_djia_constituents():
    """Fetches and loads list of DJIA constituents to `data/ticker.csv` file. Uses FMP API to get the latest data and requires `FMP_API_KEY` env variable to be set. Fetches the data from endpoint defined in `constants.DJIA_CONSTITUENTS_URL`"""
    # fetch data
    api_key = os.environ["FMP_API_KEY"]
    params = {"apikey": api_key}
    res = requests.get(DJIA_CONSTITUENTS_URL, params=params)
    res = res.json()

    # parse and validate data
    constituents = parse_obj_as(List[Constituent], res)

    # load data
    constituents = [constituent.dict() for constituent in constituents]
    keys = constituents[0].keys()

    with open("data/tickers.csv", 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(constituents)
