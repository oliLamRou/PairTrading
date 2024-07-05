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

    #Sector
    def _ticker_by_sic(self, sic: str, sic_type) -> list:
        sic_code_df = self.sic_code()
        codes = sic_code_df[sic_code_df[sic_type] == sic]['sic_code']
        
        ticker_details_df = self.__polygon_db.get_table('ticker_details')
        return ticker_details_df[
                (ticker_details_df.sic_code >= codes.min()) & 
                (ticker_details_df.sic_code <= codes.max())
            ].ticker.to_list()

    def ticker_by_office(self, sic: str) -> list:
        return self._ticker_by_sic(sic, 'office')

    def ticker_by_industry(self, sic: str) -> list:
        return self._ticker_by_sic(sic, 'industry_title')

    def filter(self):
        pass
        #sector
        #price
        #avg_vol

    def update_db(self):
        self.min_price = 10
        self.max_price = 50
        self.min_vol = 1000000
        df = self.filtered_tickers
        print(len(df.ticker))
        for ticker in df.ticker:
            print(f'/// Doing {ticker}')
            if not self._DataWrangler__polygon_db.has_value('ticker_details', 'ticker', ticker):
                df = self.ticker_info(ticker)
                time.sleep(15)

            df = self.market_data(ticker)
            if df.empty:
                self.market_data(ticker, update=True)
                time.sleep(15)

if __name__ == '__main__':
    s = Scanner()
    s.update_db()
