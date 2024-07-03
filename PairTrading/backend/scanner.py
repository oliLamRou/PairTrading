import pandas as pd
import numpy as np
from PairTrading.backend.data import Data
import math

class Scanner(Data):
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
        self.
        self._filtered_tickers = []

    @property
    def filtered_tickers(self):
        if not self._filtered_tickers:
            df = self.grouped_daily()
            df = df[
                (df.close >= self.min_price) &
                (df.close <= self.max_price) &
                (df.close >= self.min_vol) &
                (df.close >= self.max_vol)
            ]

        return self._filtered_tickers


if __name__ == '__main__':
    f = Scanner()
    # f.filter_by_price(min_price=1000000)
    df = f.grouped_daily()
    print(df.columns)