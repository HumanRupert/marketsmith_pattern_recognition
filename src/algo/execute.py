import datetime

import backtrader as bt

from src.constants import STARTING_CASH, TICKER
import src.algo.strategies as strats


def exec(patterns):
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(STARTING_CASH)

    data = bt.feeds.YahooFinanceCSVData(dataname=f"data/{TICKER}.csv")
    cerebro.adddata(data)

    cerebro.addstrategy(strats.CupWithHandleStrategy, patterns)

    cerebro.broker.set_coc(True)

    print('Starting Portfolio Value: %.1f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.1f' % cerebro.broker.getvalue())


if __name__ == '__main__':
    exec()
