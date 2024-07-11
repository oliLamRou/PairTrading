import os
import configparser
import time
from datetime import timedelta
import warnings

import pandas as pd
import requests
import yfinance

from PairTrading.backend.database import DataBase
from PairTrading.backend.polygon import Polygon
from PairTrading.src import _constant
from PairTrading.src.utils import PROJECT_ROOT

#DATA HANDLER
class DataWrangler(DataBase, Polygon):
    POLYGON_DB = (PROJECT_ROOT / 'data' / 'polygon.db').resolve()
    YFINANCE_DB = (PROJECT_ROOT / 'data' / 'market_data' / 'yfinance.db').resolve()

    TICKER_INFO_TABLE_NAME = 'ticker_details'
    MARKET_DATA_TABLE_NAME = 'market_data'
    MARKET_SNAPSHOT_TABLE_NAME = 'grouped_daily'
    SIC_CODE_TABLE_NAME = 'sic_code'
    TICKER_TYPES_TABLE_NAME = 'ticker_types'

    def __init__(self):
        Polygon.__init__(self)
        self.__polygon_db = DataBase(path = self.POLYGON_DB)
        self.__yfinance_db = DataBase(path = self.YFINANCE_DB)

        #Properties
        self._all_ticker_info = pd.DataFrame()
        self._all_market_data = pd.DataFrame()
        self._sic_code = pd.DataFrame()
        self._ticker_types = pd.DataFrame()
        self._market_snapshot = pd.DataFrame()

        self.setup_polygon()
        self.setup_yfinance()

    def setup_user(self):
        pass

    def setup_yfinance(self):
        #market_data
        self.__polygon_db.setup_table(
            self.MARKET_DATA_TABLE_NAME,
            self._renamed_columns(_constant.YFINANCE_MARKET_DATA_COLUMNS)
        )

    def setup_polygon(self):
        #market_data
        self.__polygon_db.setup_table(
            self.MARKET_DATA_TABLE_NAME,
            self._renamed_columns(_constant.MARKET_DATA_COLUMNS)
        )

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

        if not self.__polygon_db.has_value(self.TICKER_INFO_TABLE_NAME, 'ticker', ticker) or update:
            results = self.ticker_details(ticker)

            print(f'{self.TICKER_INFO_TABLE_NAME} --> ("Updating" if update else "Adding"): {" ".join(str(r) for r in results.values())[:60]} ...\n')
            if update:
                self.__polygon_db.update_row(self.TICKER_INFO_TABLE_NAME, results, 'ticker', ticker)
            else:
                self.__polygon_db.add_row(self.TICKER_INFO_TABLE_NAME, results)
            
            self.__polygon_db._commit

            #Reload table
            self._all_ticker_info = self.__polygon_db.get_table(self.TICKER_INFO_TABLE_NAME)

        return self.all_ticker_info[self.all_ticker_info.ticker == ticker]

    def market_data(self,
            ticker: str,
            timespan: str = 'day',
            n_days: int = 300,
            update: bool = False
        ) -> pd.DataFrame():
        #NOTE: ticker has a list. [] = all, [ticker, ...]

        table_name = self.MARKET_DATA_TABLE_NAME
        if update:
            self.__polygon_db._delete_rows(table_name, 'ticker', ticker)
            results = self.aggregates(ticker)
            print(f"{table_name} --> Clearing and downloading rows for {ticker}")
            for result in results:
                result['ticker'] = ticker
                result['timespan'] = 'd'
                self.__polygon_db.add_row(table_name, result)

            print(f'Last row: {result}\n')
            self.__polygon_db._commit

        df = self.__polygon_db.get_table(table_name)
        #NOTE: return from a list of ticker
        return df[(df.ticker == ticker) & (df.timespan == 'd')]

    def y_market_data(self):
        path = '../../data/yfinance'
        self.__yfinance_db.setup_table(
            'market_data',
            self._renamed_columns(_constant.YFINANCE_COLUMNS)
        )
        for file in os.listdir(path):
            if file == '.DS_Store':
                continue

            ticker = file.replace('.csv', '')
            print(ticker)
            df = pd.read_csv(path + '/' + file)
            self.__yfinance_db._delete_rows('market_data', 'ticker', ticker)
            for i, row in df.iterrows():
                row = row.to_dict()
                row['ticker'] = ticker
                row['timespan'] = 'd'
                row = self.format_results(row, _constant.YFINANCE_COLUMNS)
                self.__yfinance_db.add_row('market_data', row)

        self.__yfinance_db._commit
        print(self.__yfinance_db.get_table('market_data'))


if __name__ == '__main__':
    dw = DataWrangler()
    # dw.y_market_data()


