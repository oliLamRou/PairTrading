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

class Data(DataBase, Polygon):
    DB = (PROJECT_ROOT / 'data' / 'polygon.db').resolve()

    def __init__(self):
        DataBase.__init__(self, path=self.DB)
        Polygon.__init__(self)
        
    def get_renamed_columns(self, columns: dict) -> dict:
         return {v[0]: v[1] for v in columns.values()}

    def get_grouped_daily(self, 
            table_name: str = 'grouped_daily',
            update: bool = False
        ) -> pd.DataFrame():

        self.setup_table(
            table_name, 
            self.get_renamed_columns(_constant.GROUPED_DAILY_COLUMNS)
        )
        if update:
            print(f"--> Clearing and downloading: {table_name}\n")
            self.clear_table(table_name) #NOTE: this need to be a insert missing
            
            results = self.grouped_daily()
            for result in results:
                self.add_row(table_name, result)

        return self.get_table(table_name)

    def get_ticker_details(self,
            ticker: str,
            table_name: str = 'ticker_details',
            update: bool = False
        ) -> pd.DataFrame():

        #Create and add whatever is missing
        self.setup_table(
            table_name, 
            self.get_renamed_columns(_constant.TICKER_DETAILS_COLUMNS)
        )
        
        if not self.has_value(table_name, 'ticker', ticker):
            results = self.ticker_details(ticker)
            print(f'Adding: {" ".join(str(r) for r in results.values())[:60]} ...\n')
            self.add_row(table_name, results)
        elif update:
            results = self.ticker_details(ticker)
            print(f'Updating: {" ".join(str(r) for r in results.values())[:60]} ...\n')
            self.update_row(table_name, results, 'ticker', ticker)

        return self.get_rows(table_name, 'ticker', ticker)

    def get_ticker_types(self,
            table_name: str = 'ticker_types',
            asset_class: str = 'stocks',
            locale: str = 'us',
            update: bool = False
        ) -> pd.DataFrame():

        self.setup_table(
            table_name, 
            self.get_renamed_columns(_constant.TICKER_TYPES_COLUMNS)
        )

        if update:
            print(f"--> Clearing and downloading: {table_name}\n")
            self.clear_table(table_name)
            results = self.ticker_types(asset_class, locale)
            for result in results:
                self.add_row(table_name, result)

        return self.get_table(table_name)

    def get_aggregates(self,
            ticker: str,
            timespan: str = 'day',
            n_days: int = 300,
            update: bool = False
        ) -> pd.DataFrame():
        #NOTE: need to return df
        #I think we should merge all daily table in 1

        table_name = f'{timespan}_{ticker}'
        self.setup_table(
            table_name,
            self.get_renamed_columns(_constant.AGGREGATES_COLUMNS)
        )

        if update:
            self.clear_table(table_name)
            results = self.aggregates(ticker)
            print(f"--> Clearing and downloading: {table_name}\n")
            for result in results:
                self.add_row(table_name, result)

        return self.get_table(table_name)

if __name__ == '__main__':
    p = Data()
    df = p.get_aggregates('MSTR', update=True)
    print(df)
