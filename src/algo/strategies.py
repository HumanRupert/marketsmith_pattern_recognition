import datetime
from typing import List

import backtrader as bt
from backtrader.utils import num2date
import pandas as pd

from src.constants import TICKER
from src.models import CupWithHandle


class CupWithHandleStrategy(bt.Strategy):
    def __init__(self, cup_with_handles):
        self.df = pd.read_csv(f"data/{TICKER}.csv", index_col="Date")
        self.df.index = pd.to_datetime(self.df.index).date

        self.dt = self.datas[0].datetime
        self.patterns = cup_with_handles

        print(f"received {len(patterns)} patterns...")

    def get_price_at_pivot_price(self, pattern: CupWithHandle):
        pivot_date = pattern.pivotPriceDate
        date_row = self.df.loc[pivot_date]
        return date_row["Close"]

    def get_recent_pattern(self):
        date = self.dt.date(0)
        for pattern in self.patterns:
            handle_end = pattern.handleLowDate
            difference = (date - handle_end).days
            if(difference > 0 and difference < 28):
                return pattern

    def log(self, txt):
        print('%s, %s' % (self.dt.date(0), txt))

    def on_no_position(self):
        # get most recent pattern
        recent_pattern = self.get_recent_pattern()
        if(recent_pattern == None):
            return  # if none, jump the bar

        # get pivot price of the pattern
        pivot_price = self.get_price_at_pivot_price(recent_pattern)
        # check if reached the price
        current_price = self.datas[0].close[0]
        if(current_price >= pivot_price):
            self.ongoing_pattern = recent_pattern
            size = self.broker.get_cash() / current_price
            self.buy(size=size)
            self.log_order(True)

    def log_order(self, is_buy: bool):
        order_type = "BUY" if is_buy else "CLOSE"
        self.log(f"Submitted {order_type} order...")
        print(f"At price: {self.datas[0].close[0]}")

    def on_exposed(self):
        # close above 15% of pivot
        pivot_price = self.get_price_at_pivot_price(self.ongoing_pattern)
        current_price = self.datas[0].close[0]
        if(current_price >= pivot_price * 1.15):
            self.close()
            self.log_order(False)

        # or below 5% of it
        if(current_price <= pivot_price * .95):
            self.close()
            self.log_order(False)

        # or if 28 days has been passed since handle end
        current_date = date = self.dt.date(0)
        handle_end = self.ongoing_pattern.handleLowDate
        difference = (current_date - handle_end).days
        if(difference >= 28):
            self.close()
            self.log_order(False)

    def next(self):
        if(self.position.size <= 0):
            self.on_no_position()
        else:
            self.on_exposed()
