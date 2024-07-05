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
    polygon_db_path = (PROJECT_ROOT / 'data' / 'polygon.db').resolve()

    def __init__(self):
        Polygon.__init__(self)
        self.__polygon_db = DataBase(path = self.polygon_db_path)
        
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

    def ticker_info(self,
            ticker: str,
            table_name: str = 'ticker_details',
            update: bool = False
        ) -> pd.DataFrame():

        #Create and add whatever is missing
        self.__polygon_db.setup_table(
            table_name, 
            self._renamed_columns(_constant.TICKER_DETAILS_COLUMNS)
        )

        if not self.__polygon_db.has_value(table_name, 'ticker', ticker):
            results = self.ticker_details(ticker)
            print(f'{table_name} --> Adding: {" ".join(str(r) for r in results.values())[:60]} ...\n')
            self.__polygon_db.add_row(table_name, results)
            self.__polygon_db._commit
        elif update:
            results = self.ticker_details(ticker)
            print(f'{table_name} --> Updating: {" ".join(str(r) for r in results.values())[:60]} ...\n')
            self.__polygon_db.update_row(table_name, results, 'ticker', ticker)
            self.__polygon_db._commit

        return self.__polygon_db.get_rows(table_name, 'ticker', ticker)

    def market_data(self,
            ticker: str,
            timespan: str = 'day',
            n_days: int = 300,
            update: bool = False
        ) -> pd.DataFrame():
        #NOTE: need to return df
        #I think we should merge all daily table in 1

        table_name = 'market_data'
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
        return df[(df.ticker == ticker) & (df.timespan == 'd')]

if __name__ == '__main__':
    p = DataWrangler()
