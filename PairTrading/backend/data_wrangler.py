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
    TICKER_INFO_TABLE_NAME = 'ticker_details'
    MARKET_DATA_TABLE_NAME = 'market_data'

    def __init__(self):
        Polygon.__init__(self)
        self.__polygon_db = DataBase(path = self.POLYGON_DB)
        
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

    def all_ticker_info(self):
        #Create and add whatever is missing
        self.__polygon_db.setup_table(
            self.TICKER_INFO_TABLE_NAME,
            self._renamed_columns(_constant.TICKER_DETAILS_COLUMNS)
        )

        return self.__polygon_db.get_table(self.TICKER_INFO_TABLE_NAME)

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

    def all_market_data(self) -> pd.DataFrame:
        return self.__polygon_db.get_table(self.MARKET_DATA_TABLE_NAME)

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

    def _normalize(self, column: str):
        def normalize_it(column):
            min_val = column.min()
            max_val = column.max()
            return column.apply(
                lambda x: (x - min_val) / (max_val - min_val)
            )        
        #NOTE: will need to bake normalized feature
        new_col = f'{column}_'
        self.__polygon_db.add_columns('market_data', {new_col: 'REAL'})
        all_df = self.all_market_data()
        for ticker in all_df['ticker'].unique():
            df = all_df[all_df['ticker'] == ticker].copy()
            df[new_col] = normalize_it(df.close)
            for i, row in df.iterrows():
                if self.__polygon_db.get_rows('market_data', 'id', row['id']).empty:
                    print(i, row)
                    continue
                self.__polygon_db.update_row('market_data', row.drop('id').to_dict(), 'id', row['id'])
                # print(self.__polygon_db.get_rows('market_data', 'id', row['id']))

        self.__polygon_db._commit

if __name__ == '__main__':
    def normalize_it(column):
        min_val = column.min()
        max_val = column.max()
        return column.apply(
            lambda x: (x - min_val) / (max_val - min_val)
        ) 
    p = DataWrangler()
    print(p.sic_code()['industry_title'].sort_values().unique())
    print(p.sic_code()['office'].value_counts().sort_values())
    # # p._normalize('close')
    # # print((p.all_market_data()))
    # import seaborn as sns
    # df = p.all_market_data()
    # df = df.sort_values('timestamp')
    # df = df[df.ticker == 'AA']
    # df['close__'] = normalize_it(df.close)
    # print(df[['close_', 'close__']])
    # df.to_csv('../test.csv', index=False)
