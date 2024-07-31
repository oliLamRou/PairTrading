import time
import pandas as pd
import yfinance as yf

from PairTrading.backend.database import DataBase
from PairTrading.src import _constant
from PairTrading.backend import _db_constant

class YahooWrangler:
    def __init__(self):
        self.__yfinance_db = DataBase(_db_constant.YFINANCE_DB)
        
    def write_market_data(self, df):
        for i, row in df.iterrows():
            row = row.to_dict()
            self.__yfinance_db.add_row(_db_constant.MARKET_DATA_TABLE_NAME, row)

    def manage_wrong_tickers(self, tickers):
        previous_failed_tickers = self.__yfinance_db.get_rows(_db_constant.FAILED_TICKER_TABLE_NAME, 'ticker', tickers).ticker.unique()
        downloaded_tickers = self.__yfinance_db.get_rows(_db_constant.MARKET_DATA_TABLE_NAME, 'ticker', tickers).ticker.unique()
        failed_to_download = set(tickers).difference(downloaded_tickers)
        failed_to_download = failed_to_download.difference(previous_failed_tickers)

        #print(f'--> Adding {failed_to_download} to {_db_constant.FAILED_TICKER_TABLE_NAME}')
        self.__yfinance_db.add_rows(_db_constant.FAILED_TICKER_TABLE_NAME, [tuple([ticker]) for ticker in failed_to_download], ['ticker'])

    def market_data(self,
            tickers: list,
            timespan: str = 'd',
            period: str = '1y',
            update: bool = False
        ) -> pd.DataFrame():

        #type check
        if type(tickers) not in [list, set, tuple]:
            raise ValueError('tickers must be type list')

        #Start with download everything
        good_tickers = set(tickers)

        #to_download minus tickers that previously failed to download
        previous_failed_tickers = self.__yfinance_db.get_rows(_db_constant.FAILED_TICKER_TABLE_NAME, 'ticker', tickers).ticker.unique()
        good_tickers = good_tickers.difference(previous_failed_tickers)

        if update:
            self.__yfinance_db._delete_rows(_db_constant.MARKET_DATA_TABLE_NAME, 'ticker', good_tickers)
        else:
            downloaded_tickers = self.__yfinance_db.get_rows(_db_constant.MARKET_DATA_TABLE_NAME, 'ticker', tickers).ticker.unique()
            good_tickers = good_tickers.difference(downloaded_tickers)
            #print(f'--> Trying to download: {good_tickers}\n')

        self.download_market_data(good_tickers, timespan, period)
        self.manage_wrong_tickers(tickers)

        # READ and RETURN
        df = self.__yfinance_db.get_rows(_db_constant.MARKET_DATA_TABLE_NAME, 'ticker', tickers)
        df.date = pd.to_datetime(df.date)
        return df

    def download_market_data(self, good_tickers, timespan, period):
        if not good_tickers:
            return 

        df = yf.download(good_tickers, period=period)
        if df.empty:
            return

        if isinstance(df.columns, pd.MultiIndex):
            df = df.stack(level='Ticker', future_stack=True).reset_index().sort_values(['Ticker', 'Date'])
        else:
            df = df.reset_index()
            df['ticker'] = good_tickers.pop()

        df.rename(columns={k: v[0] for k, v in _constant.MARKET_DATA_COLUMNS.items()}, inplace=True)
        df['timespan'] = timespan
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')
        df = df[df.close.notna()]

        #WRITE
        columns = df.columns.to_list()
        rows = [tuple(row.to_list()) for i, row in df.iterrows()]
        self.__yfinance_db.add_rows(_db_constant.MARKET_DATA_TABLE_NAME, rows, columns)


if __name__ == '__main__':
    yw = YahooWrangler()
    tickers = ['COOP', 'MSTR']
    df = yw.market_data(tickers, update=False, period='1mo')
    print(df)
