import pandas as pd
import yfinance as yf

from PairTrading.backend import yahoo_session, yahoo_engine
from PairTrading.backend.models import MarketData, FailedTicker

class YahooWrangler:
    def manage_wrong_tickers(self, tickers):
        query = yahoo_session.query(FailedTicker).filter(FailedTicker.Ticker.in_(tickers))
        previous_failed_tickers = pd.read_sql_query(query.statement, yahoo_engine).ticker.unique()
        
        query = yahoo_session.query(MarketData).filter(MarketData.Ticker.in_(tickers))
        downloaded_tickers = pd.read_sql_query(query.statement, yahoo_engine).ticker.unique()
        
        failed_to_download = set(tickers).difference(downloaded_tickers)
        failed_to_download = failed_to_download.difference(previous_failed_tickers)

        if failed_to_download:
            print(f'--> Adding {failed_to_download} to {FailedTicker.__table__}')
            rows = [{'Ticker': ticker} for ticker in failed_to_download]
            yahoo_session.bulk_insert_mappings(FailedTicker, rows)

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
        query = yahoo_session.query(FailedTicker).filter(FailedTicker.Ticker.in_(tickers))
        previous_failed_tickers = pd.read_sql_query(query.statement, yahoo_engine).ticker.unique()
        good_tickers = good_tickers.difference(previous_failed_tickers)

        if update:
            yahoo_session.query(MarketData).filter(MarketData.Ticker.in_(good_tickers)).delete()
        else:
            query = yahoo_session.query(MarketData).filter(MarketData.Ticker.in_(tickers))
            downloaded_tickers = pd.read_sql_query(query.statement, yahoo_engine).ticker.unique()
            good_tickers = good_tickers.difference(downloaded_tickers)
            
        if good_tickers:
            self.download_market_data(good_tickers, timespan, period)
            
        self.manage_wrong_tickers(tickers)
        yahoo_session.commit()

        # READ and RETURN
        query = yahoo_session.query(MarketData).filter(MarketData.Ticker.in_(tickers))
        df = pd.read_sql_query(query.statement, yahoo_engine)
        if not df.empty:
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
            df['Ticker'] = good_tickers.pop()

        df['Timespan'] = timespan
        df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
        df = df[df.Close.notna()]

        #WRITE
        yahoo_session.bulk_insert_mappings(MarketData, df.to_dict(orient='records'))
        print(f'Adding {",".join(df.Ticker.unique())} to {MarketData.__table__}')

if __name__ == '__main__':
    yw = YahooWrangler()
    df = yw.market_data(['ARKK', 'IBIT', 'F', 'T', 'AAPL'], update=False)
    print(df.date)