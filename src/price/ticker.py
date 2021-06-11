import os
import csv
from typing import List

import requests
from dotenv import load_dotenv
from pydantic import parse_obj_as

from src.price.endpoints import NASDAQ100_CONSTITUENTS, DJIA_CONSTITUENTS
from src.models import Constituent

load_dotenv()


def load_tickers(endpoint: str, api_key: str = os.environ["FMP_API_KEY"]) -> None:
    """Fetches and loads list of tickers to `data/ticker.csv` file. Uses FMP API to get the latest data and requires `FMP_API_KEY` env variable to be set. Fetches the data from the passed endpoint."""
    params = {"apikey": api_key}
    res = requests.get(endpoint, params=params)
    res = res.json()

    # parse and validate data
    tickers = parse_obj_as(List[Constituent], res)

    # write data to file
    tickers = [constituent.dict() for constituent in tickers]
    keys = tickers[0].keys()
    with open("data/tickers.csv", 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(tickers)


if __name__ == "__main__":
    load_tickers(DJIA_CONSTITUENTS)
