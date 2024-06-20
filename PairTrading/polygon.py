import pandas as pd
import requests
import configparser
import io
import os
import random
import json
import time
from datetime import timedelta

class Polygon:
    ALL_SYMBOLS_PATH = '../data/all_symbol.csv'

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('../.config.ini')

        #Key
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

    def get_data(self, url):
        #400 bad requests
        #429 too many requests
        #200 good

        r = requests.get(self.base_url + url)
        if not r.status_code == 200:
            print(r)
            return pd.DataFrame()

        results = r.json().get('results')
        if results == None:
            return pd.DataFrame()

        index = list(range(len(results)))
        return pd.concat([pd.DataFrame(results, index=index)])


    def grouped_daily(self, update=False):
        path = '../data/grouped_daily.csv'
        if os.path.exists(path) and not update:
            return pd.read_csv(path)

        url = f'v2/aggs/grouped/locale/us/market/stocks/{self.previous_day}?adjusted=true&apiKey={self.key}'
        df = self.get_data(url)
        df.to_csv(path, index=False)
        return df

    def historical(self, symbol):
        end = self.today.strftime('%Y-%m-%d')
        start = (self.today - timedelta(days=300)).strftime('%Y-%m-%d')
        url = f'v2/aggs/ticker/{symbol}/range/1/day/{start}/{end}?adjusted=true&sort=asc&apiKey={self.key}'
        df = self.get_data(url)
        print(df)
        if df.empty:
            return True
        
        df.to_csv(f'../data/historical/{symbol}.csv', index = False)



if __name__ == '__main__':
    p = Polygon()
    gd = p.grouped_daily(update=True)
    print(gd)


    # tickers = gd[(gd['c'] > 20) & (gd['c'] < 50) & (gd['v'] > 1000000)]['T'].to_list()
    # for symbol in tickers:
    #     x = p.historical(symbol)
    #     if x:
    #         break

    #     time.sleep(15)

    #get yesterday snapshot
    #prefilter based on price and vol
    #get stocks 2 years data