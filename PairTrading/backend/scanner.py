import time
import pandas as pd
import numpy as np
from PairTrading.backend.data_wrangler import DataWrangler
import math
import matplotlib.pyplot as plt
import itertools

class Scanner(DataWrangler):
    """
    GOAL: scan and filter tickers for potential pair. NO CHART
    """
    def __init__(self):
        super().__init__()
        self._pair_df = pd.DataFrame()

        #Sector
        self.office = None
        self.industry = None

        #Ticker Details
        self.min_price = 0
        self.max_price = 1000000
        self.min_vol = 0
        self.max_vol = 1000000000000

        #Market Data
        self.avg_length = 30
        self.avg_vol = 1000000

        #Pair
        self.avg_length_for_ratio = 90

        self.tickers = set(self.all_ticker_info['ticker'].to_list())
        self.bad_tickers = []

    @property
    def pair_df(self):
        pass

    #Sector
    def _sic_code(self, sic: str, sic_type) -> list:
        sic_code_df = self.sic_code()
        codes = sic_code_df[sic_code_df[sic_type] == sic]['sic_code']
        
        return self.all_ticker_info[self.all_ticker_info.sic_code.isin(codes)].ticker.to_list()

    @property
    def sic_by_office(self) -> list:
        return self._sic_code(self.office, 'office')

    @property
    def sic_by_industry(self) -> list:
        return self._sic_code(self.industry, 'industry_title')

    #Snapshot filter
    @property
    def snapshot_filter(self) -> list:
        market_snapshot_df = self.market_snapshot()
        return market_snapshot_df[
            (market_snapshot_df.close >= self.min_price) &
            (market_snapshot_df.close <= self.max_price) & 
            (market_snapshot_df.volume >= self.min_vol) & 
            (market_snapshot_df.volume <= self.max_vol)
        ]['ticker'].to_list()

    @property
    def avg_volume_filter(self) -> list:
        market_data_df = self.all_market_data.pivot(index='timestamp', columns='ticker', values='volume')
        tickers = market_data_df[-self.avg_length:].mean() > self.avg_vol
        return tickers[tickers].index.to_list()

    @property
    def filtered_tickers(self) -> set():
        #Price and Volume from a snapshot
        self.tickers = self.tickers.intersection(self.snapshot_filter)

        #avg volume
        self.tickers = self.tickers.intersection(self.avg_volume_filter)
        return self.tickers


    def get_pairs(self) -> pd.DataFrame():
        tickers = self.filtered_tickers
        market_data = self.all_market_data.pivot(index='timestamp', columns='ticker', values='close')
        market_data = (market_data - market_data.min()) / (market_data.max() - market_data.min())
        
        pair_df = pd.DataFrame()
        for i, row in self.sic_code().iterrows():
            sic_code = row.sic_code
            industry_title = row.industry_title

            industry_tickers = self.all_ticker_info[self.all_ticker_info['sic_code'] == sic_code]['ticker'].to_list()
            if len(industry_tickers) < 3:
                continue
 
            for A, B in list(itertools.combinations(tickers.intersection(industry_tickers), 2)):
                columns = ['A', 'B', 'ratio', 'industry_title', 'rank']
                values = [
                    A,
                    B,
                    (market_data[A] - market_data[B]).abs().mean(),
                    industry_title,
                    1
                ]
                pair_df.loc[pair_df.size, columns] = values

        return pair_df.reset_index(drop=True)

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
    s.max_price = 40
    s.min_vol = 1000000
    # df = s.filtered_tickers()
    # print(s.tickers)
    df = s.get_pairs()
    print(df)
