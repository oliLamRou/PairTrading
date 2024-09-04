from datetime import timedelta
import configparser

import pandas as pd
import requests
import warnings

from sqlalchemy import Integer, String, Float

from PairTrading.backend import CONFIG
from PairTrading.backend.models import MarketSnapshot, TickerDetails

class Polygon:
    BASE_URL = 'https://api.polygon.io/'
    def __init__(self):
        #API_KEY
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG)
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

    def _format_results(self, row: dict, model) -> dict:
        results_ = {}
        for k, v in row.items():
            column = model.__dict__[k]
            if isinstance(column.type, Integer):
                results_[k] = int(v)
            elif isinstance(column.type, Float):
                results_[k] = float(v)
            else:
                results_[k] = str(v)

        return results_

    def _requests_and_format(self, url: str, model):
        r = requests.get(self.BASE_URL + url)
        if not r.status_code == 200:
            warnings.warn(message=f'Requests code: {r.status_code}', category=Warning, stacklevel=2)
            return

        results = r.json().get('results')
        if not results:
            return

        print(f'Request for ({url}) successful')
        if type(results) == list:
            return [self._format_results(result, model) for result in results]
        
        return self._format_results(results, model)
    
    def _grouped_daily(self) -> [dict]:
        url = f'v2/aggs/grouped/locale/us/market/stocks/{self.last_close_date}?adjusted=true&apiKey={self.key}'
        return self._requests_and_format(url, MarketSnapshot)

    def _ticker_details(self, ticker: str) -> dict:
        url = f'v3/reference/tickers/{ticker}?apiKey={self.key}'
        return self._requests_and_format(url, TickerDetails)

if __name__ == '__main__':
    p = Polygon()
    x = p._grouped_daily()
    print(x)
