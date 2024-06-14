from datetime import timedelta
import configparser

import pandas as pd

from PairTrading.backend.market_data import MarketData
from PairTrading.src import _constant
from PairTrading.src.utils import PROJECT_ROOT

class Polygon(MarketData):
    BASE_URL = 'https://api.polygon.io/'
    def __init__(self):
        super().__init__(self.BASE_URL)

        #API_KEY
        self.config = configparser.ConfigParser()
        self.config.read(_constant.CONFIG)
        self.key = self.config['polygon']['API_KEY']

        #Date 
        self.today = pd.Timestamp.now(tz='US/Eastern')
        self._previous_day = None

    @property
    def previous_day(self):
        """
        Getting APPL stock previous close day as a reference
        """
        if self._previous_day == None:
            url = f'v2/aggs/ticker/AAPL/prev?adjusted=true&apiKey={self.key}'
            results, status_code = self.requests_results(url)
            timestamp = results[0].get('t')
            self._previous_day = pd.Timestamp(timestamp, unit='ms').strftime('%Y-%m-%d')

        return self._previous_day

    def aggregates(self, ticker: str, n_days: int = 300, timespan: str = 'day') -> [dict]:
        end = self.today.strftime('%Y-%m-%d')
        start = (self.today - timedelta(days=n_days)).strftime('%Y-%m-%d')

        url = f'v2/aggs/ticker/{ticker}/range/1/{timespan}/{start}/{end}?adjusted=true&sort=asc&apiKey={self.key}'
        return self.requests_and_format(url, _constant.AGGREGATES_COLUMNS)

    def grouped_daily(self) -> [dict]:
        url = f'v2/aggs/grouped/locale/us/market/stocks/{self.previous_day}?adjusted=true&apiKey={self.key}'
        return self.requests_and_format(url, _constant.GROUPED_DAILY_COLUMNS)

    def ticker_types(self, asset_class: str = 'stocks', locale: str = 'us') -> [dict]:
        url = f'v3/reference/tickers/types?asset_class={asset_class}&locale={locale}&apiKey={self.key}'
        return self.requests_and_format(url, _constant.TICKER_TYPES_COLUMNS)

    def ticker_details(self, ticker: str) -> dict:
        url = f'v3/reference/tickers/{ticker}?apiKey={self.key}'
        return self.requests_and_format(url, _constant.TICKER_DETAILS_COLUMNS)

if __name__ == '__main__':
    p = Polygon()
    x = p.previous_day
    print(x)
