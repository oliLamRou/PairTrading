from datetime import timedelta
import configparser

import pandas as pd
import requests
import warnings

from PairTrading.src import _constant
from PairTrading.src.utils import PROJECT_ROOT

class Polygon:
    BASE_URL = 'https://api.polygon.io/'
    def __init__(self):
        #API_KEY
        self.config = configparser.ConfigParser()
        self.config.read(_constant.CONFIG)
        self.key = self.config['polygon']['API_KEY']

        #Date 
        self.today = pd.Timestamp.now(tz='US/Eastern')
        self._last_close_date = None

    @property
    def last_close_date(self):
        """
        Getting APPL stock previous close day as a reference
        """
        if self._last_close_date == None:
            url = f'v2/aggs/ticker/AAPL/prev?adjusted=true&apiKey={self.key}'
            results = requests.get(self.BASE_URL + url).json().get('results')
            timestamp = results[0].get('t')
            self._last_close_date = pd.Timestamp(timestamp, unit='ms').strftime('%Y-%m-%d')

        return self._last_close_date

    def _format_results(self, row: dict, columns: dict) -> dict:

        results_ = {}
        for k, v in row.items():
            column = columns.get(k)
            if not column:
                print(f'Column: {k} does exist in _constant.\n')
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

    def _requests_and_format(self, url: str, columns):
        r = requests.get(self.BASE_URL + url)
        if not r.status_code == 200:
            warnings.warn(message=f'Requests code: {r.status_code}', category=Warning, stacklevel=2)
            return

        results = r.json().get('results')
        if not results:
            return

        print(f'Request for ({url}) successful')
        if type(results) == list:
            return [self._format_results(result, columns) for result in results]
        
        return self._format_results(results, columns)
    
    def _aggregates(self, ticker: str, n_days: int = 300, timespan: str = 'day') -> [dict]:
        end = self.today.strftime('%Y-%m-%d')
        start = (self.today - timedelta(days=n_days)).strftime('%Y-%m-%d')

        url = f'v2/aggs/ticker/{ticker}/range/1/{timespan}/{start}/{end}?adjusted=true&sort=asc&apiKey={self.key}'
        return self._requests_and_format(url, _constant.AGGREGATES_COLUMNS)

    def _grouped_daily(self) -> [dict]:
        url = f'v2/aggs/grouped/locale/us/market/stocks/{self.last_close_date}?adjusted=true&apiKey={self.key}'
        return self._requests_and_format(url, _constant.GROUPED_DAILY_COLUMNS)

    def _ticker_types(self, asset_class: str = 'stocks', locale: str = 'us') -> [dict]:
        url = f'v3/reference/tickers/types?asset_class={asset_class}&locale={locale}&apiKey={self.key}'
        return self._requests_and_format(url, _constant.TICKER_TYPES_COLUMNS)

    def _ticker_details(self, ticker: str) -> dict:
        url = f'v3/reference/tickers/{ticker}?apiKey={self.key}'
        return self._requests_and_format(url, _constant.TICKER_DETAILS_COLUMNS)

if __name__ == '__main__':
    p = Polygon()
    print(p.grouped_daily())
