import pandas as pd
import warnings

from PairTrading.backend.database import DataBase
from PairTrading.src import _constant
from PairTrading.backend import _db_constant

class UserWrangler(DataBase):
    def __init__(self):
        self.__user_db = DataBase(_db_constant.USER_DB)

    def get_tickers_in_allcap(self, tickers: list) -> list:
        return [ticker.upper() for ticker in tickers]

    #PAIR INFO
    def is_good_pair(self, tickers: list):
        if type(tickers) != list or len(tickers) != 2:
            raise ValueError(f'tickers:({tickers}) must be a list of 2 elements')

    def get_pair_info(self, tickers: list) -> pd.Series():
        tickers = self.get_tickers_in_allcap(tickers)        
        #Return 1 row if valid pair of 2 tickers
        self.is_good_pair(tickers)
        tickers.sort()
        df = self.__user_db.get_rows(_db_constant.PAIR_INFO_TABLE_NAME, 'pair', ['__'.join(tickers)])
        if df.empty:
            return pd.Series()

        return df.iloc[0]

    def get_pairs_in_watchlist(self, watchlist: str) -> pd.DataFrame():
        #return all rows with 1 in watchlist col
        return self.__user_db.get_rows(_db_constant.PAIR_INFO_TABLE_NAME, 'watchlist', 1)

    def is_watchlist(pair: list) -> bool:
        #return watchlist value
        pair = self.get_tickers_in_allcap(pair)
        return self.get_pair_info(pair).fillna(0)['watchlist']

    def format_pair_info_dict(self, tickers: list, pair_info: dict) -> dict:
        tickers = self.get_tickers_in_allcap(tickers)
        tickers.sort()
        pair_info = pair_info.copy()
        pair_info['A'] = tickers[0]
        pair_info['B'] = tickers[1]
        pair_info['pair'] = '__'.join(tickers)
        return pair_info

    def update_pair_info(self, tickers: list, pair_info: dict) -> pd.Series():
        self.is_good_pair(tickers)

        pair_info = self.format_pair_info_dict(tickers, pair_info)
        print('dict', pair_info)

        if self.__user_db.has_value(_db_constant.PAIR_INFO_TABLE_NAME, 'pair', pair_info['pair']):
            self.__user_db.update_row(_db_constant.PAIR_INFO_TABLE_NAME, pair_info, 'pair', pair_info['pair'])
            print(f'Updating: {pair_info["pair"]}')
        else:
            self.__user_db.add_row(_db_constant.PAIR_INFO_TABLE_NAME, pair_info)
            print(f'Adding: {pair_info["pair"]}')

        return self.get_pair_info(tickers)

    #RANK
    def get_ticker_rank(self, ticker: str) -> int:
        df = self.__user_db.get_rows(_db_constant.TICKER_RANK_TABLE_NAME, 'ticker', [ticker])
        if df.empty:
            return None

        return df['rank'].iloc[0]

    def set_ticker_rank(self, ticker: str, rank: int) -> int:
        values = _constant.TICKER_RANK_COLUMNS.copy()
        values['ticker'] = ticker
        values['rank'] = rank
        if self.__user_db.has_value(_db_constant.TICKER_RANK_TABLE_NAME, 'ticker', ticker):
            self.__user_db.update_row(_db_constant.TICKER_RANK_TABLE_NAME, values, 'ticker', ticker)
        else:
            self.__user_db.add_row(_db_constant.TICKER_RANK_TABLE_NAME, values)

        return self.get_ticker_rank(ticker)

if __name__ == '__main__':
    uw = UserWrangler()
    print(uw.get_pair_info(['ARKK', 'ARKG']))