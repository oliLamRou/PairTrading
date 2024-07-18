import os
import configparser
import time
from datetime import timedelta
import warnings

import pandas as pd
import requests
import yfinance as yf

from PairTrading.backend.database import DataBase
from PairTrading.backend.polygon import Polygon
from PairTrading.src import _constant
from PairTrading.src.utils import PROJECT_ROOT

#DATA HANDLER
class DataWrangler(DataBase, Polygon):
    POLYGON_DB = (PROJECT_ROOT / 'data' / 'polygon.db').resolve()
    YFINANCE_DB = (PROJECT_ROOT / 'data' / 'local' / 'yfinance.db').resolve()
    USER_DB = (PROJECT_ROOT / 'data' / 'local' / 'user.db').resolve()

    #User
    TICKER_RANK_TABLE_NAME = 'ticker_rank'

    #Yahoo
    MARKET_DATA_TABLE_NAME = 'market_data'
    FAILED_TICKER_TABLE_NAME = 'failed_ticker'

    #Polygon
    TICKER_INFO_TABLE_NAME = 'ticker_details'
    MARKET_SNAPSHOT_TABLE_NAME = 'grouped_daily'
    SIC_CODE_TABLE_NAME = 'sic_code'
    TICKER_TYPES_TABLE_NAME = 'ticker_types'

    def __init__(self):
        Polygon.__init__(self)
        self.__polygon_db = DataBase(path = self.POLYGON_DB)
        self.__yfinance_db = DataBase(path = self.YFINANCE_DB)
        self.__user_db = DataBase(path = self.USER_DB)

        #Properties
        self._all_ticker_info = pd.DataFrame()
        self._all_market_data = pd.DataFrame()
        self._sic_code = pd.DataFrame()
        self._ticker_types = pd.DataFrame()
        self._market_snapshot = pd.DataFrame()

        self.setup_polygon()
        self.setup_yfinance()
        self.setup_user()

    def setup_user(self):
        self.__user_db.setup_table(
            self.TICKER_RANK_TABLE_NAME,
            self._renamed_columns(_constant.TICKER_RANK_COLUMNS)
        )

    def setup_yfinance(self):
        #market_data
        self.__yfinance_db.setup_table(
            self.MARKET_DATA_TABLE_NAME,
            self._renamed_columns(_constant.MARKET_DATA_COLUMNS)
        )

        self.__yfinance_db.setup_table(
            self.FAILED_TICKER_TABLE_NAME,
            self._renamed_columns(_constant.FAILED_TICKER_COLUMNS)
        )

    def setup_polygon(self):
        #ticker_details
        self.__polygon_db.setup_table(
            self.TICKER_INFO_TABLE_NAME,
            self._renamed_columns(_constant.TICKER_DETAILS_COLUMNS)
        )

        #ticker_types
        self.__polygon_db.setup_table(
            self.TICKER_TYPES_TABLE_NAME,
            self._renamed_columns(_constant.TICKER_TYPES_COLUMNS)
        )

        #grouped_daily
        self.__polygon_db.setup_table(
            self.MARKET_SNAPSHOT_TABLE_NAME,
            self._renamed_columns(_constant.GROUPED_DAILY_COLUMNS)
        )
        
    @property
    def sic_code(self):
        if self._sic_code.empty:
            self._sic_code = self.__polygon_db.get_table(self.SIC_CODE_TABLE_NAME)
        
        return self._sic_code

    @property
    def all_ticker_info(self):
        if self._all_ticker_info.empty:
            self._all_ticker_info = self.__polygon_db.get_table(self.TICKER_INFO_TABLE_NAME)

        return self._all_ticker_info

    @property
    def all_market_data(self) -> pd.DataFrame:
        if self._all_market_data.empty:
            self._all_market_data = self.__yfinance_db.get_table(self.MARKET_DATA_TABLE_NAME)

        return self._all_market_data

    def _renamed_columns(self, columns: dict) -> dict:
         return {v[0]: v[1] for v in columns.values()}

    def set_ticker_rank(self, ticker, rank):
        values = _constant.TICKER_RANK_COLUMNS.copy()
        values['ticker'] = ticker
        values['rank'] = rank
        if self.__user_db.has_value(self.TICKER_RANK_TABLE_NAME, 'ticker', ticker):
            self.__user_db.update_row(self.TICKER_RANK_TABLE_NAME, values, 'ticker', ticker)
        else:
            self.__user_db.add_row(self.TICKER_RANK_TABLE_NAME, values)

    def ticker_rank(self, ticker) -> int:
        df = self.__user_db.get_rows(self.TICKER_RANK_TABLE_NAME, 'ticker', [ticker])
        if df.empty:
            return None

        return df['rank'].iloc[0]

    def market_snapshot(self, 
            update: bool = False
        ) -> pd.DataFrame():

        if update:
            print(f"--> Clearing and downloading: {self.MARKET_SNAPSHOT_TABLE_NAME}\n")
            self.__polygon_db.clear_table(self.MARKET_SNAPSHOT_TABLE_NAME)
            
            results = self.grouped_daily()
            for result in results:
                self.__polygon_db.add_row(self.MARKET_SNAPSHOT_TABLE_NAME, result)

            self.__polygon_db._commit

        if self._market_snapshot.empty:
            self._market_snapshot = self.__polygon_db.get_table(self.MARKET_SNAPSHOT_TABLE_NAME)

        return self._market_snapshot


    def ticker_info(self,
            ticker: str,
            update: bool = False
        ) -> pd.DataFrame():

        if not self.__polygon_db.has_value(
                self.TICKER_INFO_TABLE_NAME, 'ticker', ticker
                ) or update:

            results = self.ticker_details(ticker)
            if results == None:
                return

            print(f'{self.TICKER_INFO_TABLE_NAME} --> {"Updating" if update else "Adding"}: {" ".join(str(r) for r in results.values())[:60]} ...\n')
            if update:
                self.__polygon_db.update_row(self.TICKER_INFO_TABLE_NAME, results, 'ticker', ticker)
            else:
                self.__polygon_db.add_row(self.TICKER_INFO_TABLE_NAME, results)
            
            self.__polygon_db._commit

            #Reload table
            self._all_ticker_info = self.__polygon_db.get_table(self.TICKER_INFO_TABLE_NAME)

        return self.all_ticker_info[self.all_ticker_info.ticker == ticker]

    #Yahoo Finance
    def write_market_data(self, df):
        for i, row in df.iterrows():
            row = row.to_dict()
            self.__yfinance_db.add_row(self.MARKET_DATA_TABLE_NAME, row)

    def format_ticker(self, df, ticker, timespan):
        ticker_df = df.reset_index().copy()

        if isinstance(df.columns, pd.MultiIndex):
            if not ticker in ticker_df.columns.get_level_values(1).unique():
                return pd.DataFrame()

            ticker_df = df.loc[:, pd.IndexSlice[:, ticker]].reset_index()
            ticker_df.columns = ticker_df.columns.get_level_values(0)

        ticker_df.rename(columns={k: v[0] for k, v in _constant.MARKET_DATA_COLUMNS.items()}, inplace=True)
        ticker_df['ticker'] = ticker
        ticker_df['timespan'] = timespan
        ticker_df['date'] = ticker_df['date'].dt.strftime('%Y-%m-%d')
        return ticker_df

    def manage_wrong_tickers(self, tickers):
        #Manage Failed tickers
        downloaded_tickers = self.__yfinance_db.get_rows(self.MARKET_DATA_TABLE_NAME, 'ticker', tickers).ticker.unique()
        failed_to_download = set(tickers).difference(downloaded_tickers)

        for ticker in failed_to_download:
            if self.__yfinance_db.has_value(self.FAILED_TICKER_TABLE_NAME, 'ticker', ticker):
                continue

            print(f'--> Adding {ticker} to {self.FAILED_TICKER_TABLE_NAME}')
            self.__yfinance_db.add_row(self.FAILED_TICKER_TABLE_NAME, {'ticker': ticker})

        self.__yfinance_db._commit

    def market_data(self,
            tickers: list,
            timespan: str = 'd',
            period: str = '1y',
            update: bool = False
        ) -> pd.DataFrame():

        def get_rows_with_date_format(tickers):
            df = self.__yfinance_db.get_rows(self.MARKET_DATA_TABLE_NAME, 'ticker', tickers)
            df.date = pd.to_datetime(df.date)
            return df
        
        #When update skip this part so all tickers will be updated
        to_download = tickers
        if not update:
            downloaded_tickers = self.__yfinance_db.get_rows(self.MARKET_DATA_TABLE_NAME, 'ticker', tickers).ticker.unique()
            to_download = set(tickers).difference(downloaded_tickers)
            #Remove failed tickers
            to_download = to_download.difference(self.__yfinance_db.get_rows(self.FAILED_TICKER_TABLE_NAME, 'ticker', tickers).ticker.unique())

        #When to_download is empty there is nothing to update so return tickers
        if not to_download:
            return get_rows_with_date_format(tickers)

        #Download data, if nothing downloaded mean all bad tickers.
        print(f'--> Trying to download: {to_download}')
        df = yf.download(to_download, period=period)
        if df.empty:
            self.manage_wrong_tickers(tickers)
            return get_rows_with_date_format(tickers)

        #Delete all rows with tickers in to_download
        self.__yfinance_db._delete_rows(self.MARKET_DATA_TABLE_NAME, 'ticker', to_download)
        #Format and write in DB
        for ticker in to_download:
            ticker_df = self.format_ticker(df, ticker, timespan)
            if ticker_df.empty:
                continue
        
            self.write_market_data(ticker_df)

        self.__yfinance_db._commit

        self.manage_wrong_tickers(tickers)
        return get_rows_with_date_format(tickers)

if __name__ == '__main__':
    dw = DataWrangler()
    # dw._DataWrangler__user_db._drop_table('ticker_rank')
    dw.set_ticker_rank('AAPL', 0)
    print(dw.ticker_rank('AAPL'))
    # print(dw._DataWrangler__user_db.get_table('ticker_rank'))