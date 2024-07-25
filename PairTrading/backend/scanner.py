import time
import itertools

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint

from PairTrading.backend.data_wrangler import DataWrangler

class Scanner(DataWrangler):
    PAIRS_COLUMNS = ['A', 'B', 'A_avg_vol', 'B_avg_vol', 'avg_diff', 'coint', 'rank']
    def __init__(self):
        super().__init__()
        self._pair_df = pd.DataFrame()

        #Sector
        self.office = None
        self.industry = None

        #Ticker Details / snapshot
        self.min_price = 0
        self.max_price = 1000000
        self.min_vol = 0
        self.max_vol = 1000000000000

        #Market Data
        self.avg_vol_length = 30
        self.avg_vol = 1000000

        #Pair
        self.potential_pair_amount = 2
        self.avg_diff_length = 90

        self.tickers = set(self.all_ticker_info['ticker'].to_list())
        self.bad_tickers = []

    @property
    def potential_pair(self) -> pd.DataFrame():
        df = pd.DataFrame(columns = ['industry', 'potential_pair'])
        for i, row in self.sic_code.iterrows():
            sector_tickers = self.all_ticker_info[self.all_ticker_info.sic_code == row.sic_code].ticker.to_list()
            snapshot_tickers = self.snapshot_filter.intersection(sector_tickers)
            if len(snapshot_tickers) ** 2 < self.potential_pair_amount:
                continue

            df.loc[df.industry.size, ['industry', 'potential_pair']] = [row.industry_title, len(snapshot_tickers) ** 2]

        return df.sort_values('potential_pair').reset_index(drop=True)

    @property
    def sic(self) -> list:
        if self.industry:
            return self.sic_code[self.sic_code['industry_title'] == self.industry].sic_code.iloc[0]
        elif self.office:
            return self.sic_code[self.sic_code['office'] == self.office].sic_code.iloc[0]

    #Snapshot filter
    @property
    def snapshot_filter(self) -> set:
        market_snapshot_df = self.market_snapshot()
        df = market_snapshot_df[
            (market_snapshot_df.close >= self.min_price) &
            (market_snapshot_df.close <= self.max_price) & 
            (market_snapshot_df.volume >= self.min_vol) & 
            (market_snapshot_df.volume <= self.max_vol)
        ]['ticker'].to_list()
        return set(df)

    #@property
    def get_pairs(self, callback_func=None) -> pd.DataFrame():
        if not self.sic:
            return pd.DataFrame()
        
        sector_tickers = self.all_ticker_info[self.all_ticker_info.sic_code == self.sic].reset_index(drop=True).ticker.to_list()
        if not sector_tickers:
            return pd.DataFrame()

        snapshot_tickers = self.snapshot_filter.intersection(sector_tickers)
        if not snapshot_tickers:
            return pd.DataFrame()

        market_data = self.market_data(snapshot_tickers)
        tickers = market_data.ticker.sort_values().unique()

        close_data = market_data.pivot(index='date', columns='ticker', values='close')
        close_data = close_data[-self.avg_diff_length:]
        close_data = (close_data - close_data.min()) / (close_data.max() - close_data.min())

        volume_data = market_data.pivot(index='date', columns='ticker', values='volume')
        volume_data = volume_data[-self.avg_vol_length:]

        pair_df = pd.DataFrame()
        pairs = list(itertools.combinations(tickers, 2))
        for A, B in pairs:
            values = [
                A, B,
                volume_data[A].mean().astype(int), volume_data[B].mean().astype(int),
                (close_data[A] - close_data[B]).abs().mean().round(3),
                round(coint(close_data[A].fillna(0), close_data[B].fillna(0))[1], 3),
                1
            ]
            pair_df.loc[pair_df.size, self.PAIRS_COLUMNS] = values

            #Progress bar
            if callback_func:
                callback_func(pair_df.A.size / (len(pairs)))

        return pair_df.reset_index(drop=True)

    def update_db(self):
        self.min_price = 2
        self.max_price = 200
        self.min_vol = 100
        tickers = self.snapshot_filter
        for ticker in tickers:
            if not self._DataWrangler__polygon_db.has_value('ticker_details', 'ticker', ticker):
                print(f'/// Doing {ticker}')
                df = self.ticker_info(ticker)
                missing = set(tickers).difference(set(self._DataWrangler__polygon_db.get_table('ticker_details').ticker.to_list()))
                print(f'-> {len(missing)} to download\n')
                time.sleep(13)
            else:
                print('DONE:', ticker)

if __name__ == '__main__':
    s = Scanner()
    s.min_price = 5
    s.max_price = 200
    s.min_vol = 100
    s.industry = 'CRUDE PETROLEUM & NATURAL GAS'
    x = s.get_pairs()
    print(x)

