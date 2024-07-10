import os
import configparser
import time
from datetime import timedelta
import warnings

import pandas as pd
import requests

from PairTrading.backend.database import DataBase
from PairTrading.backend.polygon import Polygon
from PairTrading.src import _constant
from PairTrading.src.utils import PROJECT_ROOT

#DATA HANDLER
class DataWrangler(DataBase, Polygon):
    POLYGON_DB = (PROJECT_ROOT / 'data' / 'polygon.db').resolve()
    YFINANCE_DB = (PROJECT_ROOT / 'data' / 'yfinance.db').resolve()
    TICKER_INFO_TABLE_NAME = 'ticker_details'
    MARKET_DATA_TABLE_NAME = 'market_data'

    def __init__(self):
        Polygon.__init__(self)
        self.__polygon_db = DataBase(path = self.POLYGON_DB)
        self.__yfinance_db = DataBase(path = self.YFINANCE_DB)

        #Properties
        self._all_ticker_info = pd.DataFrame()
        self._all_market_data = pd.DataFrame()
        
    def _renamed_columns(self, columns: dict) -> dict:
         return {v[0]: v[1] for v in columns.values()}

    def _ticker_types(self,
            table_name: str = 'ticker_types',
            asset_class: str = 'stocks',
            locale: str = 'us',
            update: bool = False
        ) -> pd.DataFrame():

        self.__polygon_db.setup_table(
            table_name, 
            self._renamed_columns(_constant.TICKER_TYPES_COLUMNS)
        )

        if update:
            print(f"--> Clearing and downloading: {table_name}\n")
            self.__polygon_db.clear_table(table_name)
            results = self.ticker_types(asset_class, locale)
            for result in results:
                self.__polygon_db.add_row(table_name, result)

            self.__polygon_db._commit

        return self.__polygon_db.get_table(table_name)
    
    def sic_code(self):
        return self.__polygon_db.get_table('sic_code')

    #Market
    def market_snapshot(self, 
            table_name: str = 'grouped_daily',
            update: bool = False
        ) -> pd.DataFrame():

        self.__polygon_db.setup_table(
            table_name, 
            self._renamed_columns(_constant.GROUPED_DAILY_COLUMNS)
        )
        if update:
            print(f"--> Clearing and downloading: {table_name}\n")
            self.__polygon_db.clear_table(table_name) #NOTE: this need to be a insert missing
            
            results = self.grouped_daily()
            for result in results:
                self.__polygon_db.add_row(table_name, result)

            self.__polygon_db._commit

        return self.__polygon_db.get_table(table_name)

    @property
    def all_ticker_info(self):
        if self._all_ticker_info.empty:
            self.__polygon_db.setup_table(
                self.TICKER_INFO_TABLE_NAME,
                self._renamed_columns(_constant.TICKER_DETAILS_COLUMNS)
            )

            self._all_ticker_info = self.__polygon_db.get_table(self.TICKER_INFO_TABLE_NAME)

        return self._all_ticker_info

    def ticker_info(self,
            ticker: str,
            update: bool = False
        ) -> pd.DataFrame():

        #Create and add whatever is missing
        self.__polygon_db.setup_table(
            self.TICKER_INFO_TABLE_NAME,
            self._renamed_columns(_constant.TICKER_DETAILS_COLUMNS)
        )

        if not self.__polygon_db.has_value(self.TICKER_INFO_TABLE_NAME, 'ticker', ticker):
            results = self.ticker_details(ticker)
            print(f'{self.TICKER_INFO_TABLE_NAME} --> Adding: {" ".join(str(r) for r in results.values())[:60]} ...\n')
            self.__polygon_db.add_row(self.TICKER_INFO_TABLE_NAME, results)
            self.__polygon_db._commit
        elif update:
            results = self.ticker_details(ticker)
            print(f'{self.TICKER_INFO_TABLE_NAME} --> Updating: {" ".join(str(r) for r in results.values())[:60]} ...\n')
            self.__polygon_db.update_row(self.TICKER_INFO_TABLE_NAME, results, 'ticker', ticker)
            self.__polygon_db._commit

        return self.__polygon_db.get_rows(self.TICKER_INFO_TABLE_NAME, 'ticker', ticker)

    @property
    def all_market_data(self) -> pd.DataFrame:
        if self._all_market_data.empty:
            self._all_market_data = self.__yfinance_db.get_table(self.MARKET_DATA_TABLE_NAME)

        return self._all_market_data

    def market_data(self,
            ticker: str,
            timespan: str = 'day',
            n_days: int = 300,
            update: bool = False
        ) -> pd.DataFrame():
        #NOTE: ticker has a list. [] = all, [ticker, ...]

        table_name = self.MARKET_DATA_TABLE_NAME
        self.__polygon_db.setup_table(
            table_name,
            _constant.MARKET_DATA_COLUMNS
        )

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

    def format_results(self,
            row: dict, 
            columns_type: dict
        ) -> dict:

        results_ = {}
        for k, v in row.items():
            column = columns_type.get(k)
            if not column:
                print(f'Column: {k} does exist. It will be skipped.\n')
                continue

            column_name = column[0]
            column_type = column[1]
            if column_type == 'INTERGER':
                results_[column_name] = int(v)
            elif column_type == 'REAL':
                results_[column_name] = float(v)
            else:
                results_[column_name] = str(v)

        return results_

    # def y_market_data(self):
    #     path = '../../data/yfinance'
    #     self.__yfinance_db.setup_table(
    #         'market_data',
    #         self._renamed_columns(_constant.YFINANCE_COLUMNS)
    #     )
    #     for file in os.listdir(path):
    #         if file == '.DS_Store':
    #             continue

    #         ticker = file.replace('.csv', '')
    #         print(ticker)
    #         df = pd.read_csv(path + '/' + file)
    #         self.__yfinance_db._delete_rows('market_data', 'ticker', ticker)
    #         for i, row in df.iterrows():
    #             row = row.to_dict()
    #             row['ticker'] = ticker
    #             row['timespan'] = 'd'
    #             row = self.format_results(row, _constant.YFINANCE_COLUMNS)
    #             self.__yfinance_db.add_row('market_data', row)

    #     self.__yfinance_db._commit
    #     print(self.__yfinance_db.get_table('market_data'))


if __name__ == '__main__':
    dw = DataWrangler()
    dw._DataWrangler__yfinance_db._vacuum()
    # dw.y_market_data()


