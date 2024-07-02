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
        
    #     #Date 
    #     self.today = pd.Timestamp.now(tz='US/Eastern')
    #     self._previous_day = None

    # @property
    # def previous_day(self):
    #     """
    #     Getting APPL stock previous close day as a reference
    #     """
    #     if self._previous_day == None:
    #         url = f'v2/aggs/ticker/AAPL/prev?adjusted=true&apiKey={self.key}'
    #         df = self.get_data(url)
    #         self._previous_day = pd.Timestamp(df.loc[0, 't'], unit='ms').strftime('%Y-%m-%d')

    #     return self._previous_day

    # def requests_results(self, url: str) -> dict:
    #     #400 bad requests
    #     #429 too many requests
    #     #200 good

    #     r = requests.get(self.base_url + url)
    #     if not r.status_code == 200:
    #         print(r)
    #         raise ValueError(r.status_code)

    #     results = r.json().get('results')
    #     if results == None:
    #         print(f'Empty results for url: {url}. Full requests: {r}')
    #         return {}

    #     return results

    # def result_formatting(self, 
    #         row: dict, 
    #         columns_type: dict
    #     ) -> dict:

    #     results_ = {}
    #     for k, v in row.items():
    #         column = columns_type.get(k)
    #         if not column:
    #             print(f'Column: {k} does exist. It will be skipped.\n')
    #             continue

    #         column_name = column[0]
    #         column_type = column[1]
    #         if column_type == 'INTERGER':
    #             results_[column_name] = int(v)
    #         elif column_type == 'REAL':
    #             results_[column_name] = float(v)
    #         else:
    #             results_[column_name] = str(v)

    #     return results_

    # def aggregates(self,
    #         symbol: str,
    #         n_days: int = 300,
    #         update: bool = False
    #     ) -> pd.DataFrame():
    #     #NOTE: need to return df
    #     #I think we should merge all daily table in 1

    #     end = self.today.strftime('%Y-%m-%d')
    #     start = (self.today - timedelta(days=n_days)).strftime('%Y-%m-%d')
    #     timespan = 'day'
    #     table_name = f'{timespan}_{symbol}'
    #     columns = {v[0]: v[1] for v in _constant.HISTORICAL_COLUMNS.values()}

    #     url = f'v2/aggs/ticker/{symbol}/range/1/{timespan}/{start}/{end}?adjusted=true&sort=asc&apiKey={self.key}'
    #     results = self.requests_results(url)
    #     if not results:
    #         return
        
    #     self.create_table(table_name)
    #     self.clear_table(table_name)
    #     self.add_columns(table_name, columns)

    #     for row in results:
    #         self.result_formatting(row, _constant.HISTORICAL_COLUMNS)
    #         self.add_row(table_name, results_)

    # def grouped_daily(self, 
    #         table_name: str = 'grouped_daily',
    #         update: bool = False
    #     ) -> pd.DataFrame():

    #     if update:
    #         print("--> Updating: 'grouped_daily'\n")
    #         self.create_table(table_name)
    #         self.clear_table(table_name)
            
    #         columns = {v[0]: v[1] for v in _constant.GROUPED_DAILY_COLUMNS.values()}
    #         self.add_columns(table_name, columns)

    #         url = f'v2/aggs/grouped/locale/us/market/stocks/{self.previous_day}?adjusted=true&apiKey={self.key}'
    #         results = self.requests_results(url)
    #         for result in results:
    #             result_ = self.result_formatting(result, _constant.TICKER_TYPES_COLUMNS)
    #             self.add_row(table_name, result_)

    #     return self.get_table(table_name)

    # def ticker_types(self,
    #         table_name: str = 'ticker_types',
    #         asset_class: str = 'stocks',
    #         locale: str = 'us',
    #         update: bool = False
    #     ) -> pd.DataFrame():

    #     if update:
    #         print(f"--> Updating: '{table_name}'\n")
    #         self.create_table(table_name)
    #         self.clear_table(table_name)

    #         columns = {v[0]: v[1] for v in _constant.TICKER_TYPES_COLUMNS.values()}
    #         self.add_columns(table_name, columns)

    #         url = f'v3/reference/tickers/types?asset_class={asset_class}&locale={locale}&apiKey={self.key}'
    #         results = self.requests_results(url)
    #         for result in results:
    #             result_ = self.result_formatting(result, _constant.TICKER_TYPES_COLUMNS)
    #             self.add_row(table_name, result_)

    #     return self.get_table(table_name)

    def get_ticker_details(self,
            ticker: str,
            table_name: str = 'ticker_details',
            update: bool = False
        ) -> pd.DataFrame():

        #Create and add whatever is missing
        self.setup_table(table_name, _constant.TICKER_DETAILS_COLUMNS)

        if update:
            results = self.ticker_details(ticker)
            print(f'Adding: {" ".join(str(r) for r in results.values())[:60]} ... ')
            self.add_row(table_name, results)

        df = self.get_table(table_name)
        return df[df.ticker == ticker]

if __name__ == '__main__':
    p = Data()
    df = p.get_ticker_details("SPGI")
    print(df.T)
