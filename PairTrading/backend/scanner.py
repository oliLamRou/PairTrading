import time
import pandas as pd
import numpy as np
from PairTrading.backend.data_wrangler import DataWrangler
import math
import matplotlib.pyplot as plt

class Scanner(DataWrangler):
    """
    GOAL: scan and filter tickers for potential pair. NO CHART
    """
    def __init__(self):
        super().__init__()
        self.min_price = 0
        self.max_price = 1000000
        self.min_vol = 0
        self.max_vol = 1000000000000
        self.bad_tickers = []
        self._filtered_tickers = []

    @property
    def filtered_tickers(self):
        if not self._filtered_tickers:
            df = self.market_snapshot()
            self._filtered_tickers = df[
                (df.close >= self.min_price) &
                (df.close <= self.max_price) & 
                (df.volume >= self.min_vol) & 
                (df.volume <= self.max_vol)
            ]

        return self._filtered_tickers

    def update_db(self):
        self.min_price = 10
        self.max_price = 50
        self.min_vol = 1000000
        df = self.filtered_tickers
        for ticker in df.ticker:
            print(f'/// Doing {ticker}')
            df = self.ticker_info(ticker)
            time.sleep(15)

            df = self.market_data(ticker)
            if df.empty:
                self.market_data(ticker, update=True)
                time.sleep(15)

if __name__ == '__main__':
    s = Scanner()
    s.update_db()
    # print(s.get_table('ticker_details'))
    # s._delete_row('ticker_details', 'ticker', 'MSTR')