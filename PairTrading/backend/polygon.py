import configparser
import time
from datetime import timedelta

import pandas as pd
import requests

from PairTrading.backend.database import DataBase
from PairTrading.src import _constant
from PairTrading.src.utils import PROJECT_ROOT

class Polygon(DataBase):
    DB = (PROJECT_ROOT / 'data' / 'polygon.db').resolve()

    def __init__(self):
        super().__init__(path=self.DB)
        self.config = configparser.ConfigParser()
        self.config.read(_constant.CONFIG)

        #API_KEY
        self.key = self.config['polygon']['API_KEY']

        self.base_url = 'https://api.polygon.io/'
        self.all_symbols = []

        self.today = pd.Timestamp.now(tz='US/Eastern')
        self._previous_day = None

    @property
    def previous_day(self):
        """
        Getting APPL stock previous close day as a reference
        """
        if self._previous_day == None:
            url = f'v2/aggs/ticker/AAPL/prev?adjusted=true&apiKey={self.key}'
            df = self.get_data(url)
            self._previous_day = pd.Timestamp(df.loc[0, 't'], unit='ms').strftime('%Y-%m-%d')

        return self._previous_day

    def requests_results(self, url: str) -> dict:
        #400 bad requests
        #429 too many requests
        #200 good

        r = requests.get(self.base_url + url)
        if not r.status_code == 200:
            print(r)
            raise ValueError(r.status_code)

        results = r.json().get('results')
        if results == None:
            print(f'Empty results for ulr: {url}. Full requests: {r}')
            return {}

        return results

    def historical_(self, symbol, results):
        timespan = 'day'
        table_name = f'{timespan}_{symbol}'
        columns = {v[0]: v[1] for v in _constant.HISTORICAL_COLUMNS.values()}
        
        self.create_table(table_name)
        self.clear_table(table_name)
        self.add_columns(table_name, columns)

        for row in results:
            results_ = {}
            for k, v in row.items():
                column = _constant.HISTORICAL_COLUMNS.get(k)
                column_name = column[0]
                column_type = column[1]
                if column_type == 'INTERGER':
                    results_[column_name] = int(v)
                elif column_type == 'REAL':
                    results_[column_name] = float(v)
                elif column_type == 'TEXT':
                    results_[column_name] = str(v)
                else:
                    print(f'Column: {k} does exist in HISTORICAL_COLUMNS. It will be skipped.\n')
                    continue

            self.add_row(table_name, results_)

    def historical(self, 
            symbol: str,
            n_days: int = 300,
            update: bool = False
        ) -> pd.DataFrame():

        end = self.today.strftime('%Y-%m-%d')
        start = (self.today - timedelta(days=n_days)).strftime('%Y-%m-%d')
        timespan = 'day'
        table_name = f'{timespan}_{symbol}'
        columns = {v[0]: v[1] for v in _constant.HISTORICAL_COLUMNS.values()}

        url = f'v2/aggs/ticker/{symbol}/range/1/{timespan}/{start}/{end}?adjusted=true&sort=asc&apiKey={self.key}'
        results = self.requests_results(url)
        if not results:
            return
        
        self.create_table(table_name)
        self.clear_table(table_name)
        self.add_columns(table_name, columns)

        for row in results:
            results_ = {}
            for k, v in row.items():
                column = _constant.HISTORICAL_COLUMNS.get(k)
                column_name = column[0]
                column_type = column[1]
                if column_type == 'INTERGER':
                    results_[column_name] = int(v)
                elif column_type == 'REAL':
                    results_[column_name] = float(v)
                elif column_type == 'TEXT':
                    results_[column_name] = str(v)
                else:
                    print(f'Column: {k} does exist in HISTORICAL_COLUMNS. It will be skipped.\n')
                    continue

            self.add_row(table_name, results_)

    def ticker_details(self,
            table_name: str = 'ticker_details',
            update: bool = False
        ) -> pd.DataFrame():

        grouped_daily_df = self.grouped_daily(update=update)
        
        columns = _constant.TICKER_DETAILS_COLUMNS
        self.create_table(table_name)
        self.add_columns(table_name, columns)
        for ticker in grouped_daily_df['symbol'].to_list():
            self.cursor.execute(f"SELECT * FROM {table_name} WHERE {'ticker'} = ?", (ticker,))

            if self.cursor.fetchall():
                continue
            
            url = f'v3/reference/tickers/{ticker}?apiKey={self.key}'
            results = self.requests_results(url)
            
            results_ = {}
            for k, v in results.items():
                column_type = columns.get(k)
                if column_type == 'INTERGER':
                    results_[k] = int(v)
                elif column_type == 'REAL':
                    results_[k] = float(v)
                elif column_type == 'TEXT':
                    results_[k] = str(v)
                else:
                    print(f'Column: {k} does exist in TICKER_DETAILS_COLUMNS. It will be skipped.\n')
                    continue

            print(f'Adding: {" ".join(str(r) for r in results_.values())[:60]} ... ')
            self.add_row(table_name, results_)
            time.sleep(15)

    def grouped_daily(self, 
            table_name: str = 'grouped_daily',
            update: bool = False
        ) -> pd.DataFrame():

        if update:
            print("--> Updating: 'grouped_daily'\n")
            columns = _constant.GROUPED_DAILY_COLUMNS

            url = f'v2/aggs/grouped/locale/us/market/stocks/{self.previous_day}?adjusted=true&apiKey={self.key}'
            results = self.requests_results(url)
            
            self.create_table(table_name)
            self.clear_table(table_name)
            self.add_columns(table_name, columns)

            for result in results:
                result_ = {}
                for key,n_key in zip(result.keys(), columns.keys()):
                    result_[n_key] = result.get(key)

                self.add_row(table_name, result_)

        return self.get_table(table_name)

if __name__ == '__main__':
    p = Polygon()
    p.ticker_details()
    #Ticker details should only do one
    #Need a update for all those ticker function


