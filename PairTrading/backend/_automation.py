import time
import pandas as pd
from pandas import Timestamp
import numpy as np
from PairTrading.backend.scanner import Scanner
import math
import matplotlib.pyplot as plt
import itertools
import yfinance as yf

class Automation(Scanner):
    def __init__(self):
        super().__init__()

    def update_db(self):
        self.min_price = 2
        self.max_price = 200
        self.min_vol = 100
        tickers = self.snapshot_filter
        for ticker in tickers:
            if not self._PolygonWrangler__polygon_db.has_value('ticker_details', 'ticker', ticker):
                print(f'/// Doing {ticker}')
                df = self.ticker_info(ticker)
                missing = set(tickers).difference(set(self._PolygonWrangler__polygon_db.get_table('ticker_details').ticker.to_list()))
                print(f'-> {len(missing)} to download\n')
                time.sleep(13)
            else:
                print('DONE:', ticker)

if __name__ == '__main__':
    a = Automation()
    a.update_db()

