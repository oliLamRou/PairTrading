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
        #Sector
        self.office = 'Office of Energy & Transportation'
        self.industry = None

        #Ticker Details
        self.min_price = 0
        self.max_price = 1000000
        self.min_vol = 0
        self.max_vol = 1000000000000

        #Market Data
        self.avg_length = 30
        self.avg_vol = 100000

        self.bad_tickers = []

    def filtered_tickers(self):
        #Pre filter with last closing market snapshot price and volume
        market_snapshot_df = self.market_snapshot()
        tickers = market_snapshot_df[
            (market_snapshot_df.close >= self.min_price) &
            (market_snapshot_df.close <= self.max_price) & 
            (market_snapshot_df.volume >= self.min_vol) & 
            (market_snapshot_df.volume <= self.max_vol)
        ].ticker

        #Filter sector
        sic_code_df = self.sic_code()
        sic_codes = sic_code_df[
            sic_code_df.office == self.office
        ]['sic_code'].to_list()

        all_ticker_info_df = self.all_ticker_info()
        all_ticker_info_df['sic_code'] = all_ticker_info_df['sic_code'].fillna(0).astype(int)
        tickers = all_ticker_info_df[
            (all_ticker_info_df.ticker.isin(tickers)) &
            (all_ticker_info_df['sic_code'].astype(int).isin(sic_codes))
        ]['ticker']

        #Market Data
        market_data_df = self._DataWrangler__polygon_db.get_table('market_data')
        tickers_ = []
        for ticker in tickers:
            ticker_df = market_data_df[market_data_df.ticker == 'ticker']
            #If avg vol is SMALLER it skip
            if ticker_df.volume[-self.avg_length:].mean() < self.avg_vol:
                continue

            tickers_.append(ticker)

        return tickers_

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

    def update_db(self):
        self.min_price = 10
        self.max_price = 50
        self.min_vol = 1000000
        df = self.filtered_tickers()
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
    s.min_price = 10
    s.max_price = 50
    s.min_vol = 1000000
    df = s.filtered_tickers()
    print(df)
