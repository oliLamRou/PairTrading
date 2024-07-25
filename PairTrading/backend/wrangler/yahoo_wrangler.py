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

    def format_ticker(self, df, ticker, timespan):
        ticker_df = df.reset_index().copy()

        if isinstance(df.columns, pd.MultiIndex):
            if not ticker in ticker_df.columns.get_level_values(1).unique():
                return pd.DataFrame()

            ticker_df = df.loc[:, pd.IndexSlice[:, ticker]].reset_index()
            ticker_df.columns = ticker_df.columns.get_level_values(0)

        ticker_df.rename(columns={k: v[0] for k, v in _constant.MARKET_DATA_COLUMNS.items()}, inplace=True)
        ticker_df['ticker'] = ticker
        ticker_df['timespan'] = timespan
        ticker_df['date'] = ticker_df['date'].dt.strftime('%Y-%m-%d')
        return ticker_df[ticker_df.close.notna()]

    def manage_wrong_tickers(self, tickers):
        #Manage Failed tickers
        downloaded_tickers = self.__yfinance_db.get_rows(_db_constant.MARKET_DATA_TABLE_NAME, 'ticker', tickers).ticker.unique()
        failed_to_download = set(tickers).difference(downloaded_tickers)

        for ticker in failed_to_download:
            if self.__yfinance_db.has_value(_db_constant.FAILED_TICKER_TABLE_NAME, 'ticker', ticker):
                continue

            print(f'--> Adding {ticker} to {_db_constant.FAILED_TICKER_TABLE_NAME}')
            self.__yfinance_db.add_row(_db_constant.FAILED_TICKER_TABLE_NAME, {'ticker': ticker})

    def market_data(self,
            tickers: list,
            timespan: str = 'd',
            period: str = '1y',
            update: bool = False
        ) -> pd.DataFrame():

        #NOTE: remove rows with nan
        def get_rows_with_date_format(tickers):
            df = self.__yfinance_db.get_rows(_db_constant.MARKET_DATA_TABLE_NAME, 'ticker', tickers)
            df.date = pd.to_datetime(df.date)
            return df
        
        #When update skip this part so all tickers will be updated
        to_download = tickers
        if not update:
            downloaded_tickers = self.__yfinance_db.get_rows(_db_constant.MARKET_DATA_TABLE_NAME, 'ticker', tickers).ticker.unique()
            to_download = set(tickers).difference(downloaded_tickers)
            #Remove failed tickers
            to_download = to_download.difference(self.__yfinance_db.get_rows(_db_constant.FAILED_TICKER_TABLE_NAME, 'ticker', tickers).ticker.unique())

        #When to_download is empty there is nothing to update so return tickers
        if not to_download:
            return get_rows_with_date_format(tickers)

        #Download data, if nothing downloaded mean all bad tickers.
        print(f'--> Trying to download: {to_download}')
        df = yf.download(to_download, period=period)
        if df.empty:
            self.manage_wrong_tickers(tickers)
            return get_rows_with_date_format(tickers)

        #Delete all rows with tickers in to_download
        self.__yfinance_db._delete_rows(_db_constant.MARKET_DATA_TABLE_NAME, 'ticker', to_download)
        #Format and write in DB
        for ticker in to_download:
            ticker_df = self.format_ticker(df, ticker, timespan)
            if ticker_df.empty:
                continue
            
            self.write_market_data(ticker_df)

        self.manage_wrong_tickers(tickers)
        return get_rows_with_date_format(tickers)

if __name__ == '__main__':
    yw = DataWrangler()
