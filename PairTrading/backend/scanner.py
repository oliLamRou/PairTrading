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
        self.office = 'Office of Technology'
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

        self.tickers = set(self.all_ticker_info()['ticker'].to_list())
        self.bad_tickers = []

    @property
    def pair_df(self):
        pass

    #Sector
    def _sic_code(self, sic: str, sic_type) -> list:
        sic_code_df = self.sic_code()
        codes = sic_code_df[sic_code_df[sic_type] == sic]['sic_code']
        
        ticker_details_df = self.all_ticker_info()
        return ticker_details_df[
                (ticker_details_df.sic_code >= codes.min()) & 
                (ticker_details_df.sic_code <= codes.max())
            ].ticker.to_list()

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
        #NOTE: This could get 10x faster without a loop
        #Market Data
        market_data_df = self.all_market_data()
        tickers_ = []
        for ticker in self.tickers:
            ticker_df = market_data_df[
                market_data_df['ticker'] == ticker
            ]
            #If avg vol is SMALLER it skip
            if ticker_df.volume[-self.avg_length:].mean() < self.avg_vol:
                continue

            tickers_.append(ticker)

        return tickers_

    def filtered_tickers(self):
        if self.office:
            self.tickers = self.tickers.intersection(self.sic_by_office)
        
        if self.industry:
            self.tickers = self.tickers.intersection(self.sic_by_industry)

        #Price and Volume from a snapshot
        self.tickers = self.tickers.intersection(self.snapshot_filter)

        #avg volume
        self.tickers = self.tickers.intersection(self.avg_volume_filter)
        return self.tickers


    def get_pairs(self) -> pd.DataFrame():
        #NOTE: ADD OFFICE
        def normalize_it(df):
            min_val = df.close.min()
            max_val = df.close.max()
            return df.close.apply(
                lambda x: (x - min_val) / (max_val - min_val)
            )

        t = self.filtered_tickers()
        market_data = self.all_market_data().pivot(index='timestamp', columns='ticker', values='close_')
        pair_df = pd.DataFrame()
        for pair in list(itertools.combinations(t, 2)):
            pair_df.loc[pair_df.size, ['A', 'B', 'ratio']] = [pair[0], pair[1], (market_data[pair[0]] - market_data[pair[1]]).mean()]
            # pair_df.reset_index(drop=True, inplace=True)

        # pair_df.ratio.hist()
        # plt.show()
        # pair_df.to_csv('../pair_df.csv', index=False)
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

    # x = np.array(s.market_data('ASTS').close).reshape(-1, 1)
    # min_max_scaler = preprocessing.MinMaxScaler()
    # x_scaled = min_max_scaler.fit_transform(x)
    # df = pd.DataFrame(x_scaled)
    # print(df)
    # close = s.market_data('ASTS').apply(lambda x: (x-x.mean())/ x.std())
    # print(close)
    # df = s.all_market_data()
    # # print(pd.concat([df.groupby('ticker')['volume'].rolling(30).mean().tail(1)]))
    # print(pd.concat([df.groupby('ticker')['volume'].rolling(30).mean().tail(1)]))
    # # market_data_df.volume.rolling(30).mean()
