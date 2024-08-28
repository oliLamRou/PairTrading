import pandas as pd
import warnings

from PairTrading.backend import user_session, user_engine
from PairTrading.backend.models import PairInfo

class UserWrangler:
    def get_tickers_in_allcap(self, tickers: list) -> list:
        return [ticker.upper() for ticker in tickers]

    #PAIR INFO
    def is_good_pair(self, tickers: list):
        if type(tickers) != list or len(tickers) != 2:
            raise ValueError(f'tickers:({tickers}) must be a list of 2 elements')

    def get_pair_info(self, tickers: list) -> pd.Series():
        tickers = self.get_tickers_in_allcap(tickers)        
        self.is_good_pair(tickers)
        tickers.sort()
        query = user_session.query(PairInfo).filter(PairInfo.Pair.in_(['__'.join(tickers)]))
        df = pd.read_sql_query(query.statement, user_engine)
        if df.empty:
            return pd.Series()

        return df.iloc[0]

    def format_pair_info_dict(self, tickers, pair_info: dict) -> dict:
        tickers = self.get_tickers_in_allcap(tickers)
        tickers.sort()

        pair_info = pair_info.copy()
        pair_info['A'] = tickers[0]
        pair_info['B'] = tickers[1]
        pair_info['Pair'] = '__'.join(tickers)
        return pair_info

    def update_pair_info(self, pair_info: dict) -> pd.Series():
        tickers = [pair_info.get('A'), pair_info.get('B')]
        self.is_good_pair(tickers)

        pair_info = self.format_pair_info_dict(tickers, pair_info)
        del pair_info['data']

        if self.get_pair_info(tickers).empty:
            user_session.add(PairInfo(**pair_info))
            print(f'Adding: {pair_info["Pair"]}')
        else:
            user_session.query(PairInfo).filter(PairInfo.Pair == pair_info['Pair']).update(pair_info)
            print(f'Updating: {pair_info["Pair"]}')

        user_session.commit()
        return self.get_pair_info(tickers)

    # def get_pairs_in_watchlist(self, watchlist: str) -> pd.DataFrame():
    #     query = user_session.query(PairInfo).filter(PairInfo.Watchlist == watchlist)
    #     return pd.read_sql_query(query.statement, user_engine)

if __name__ == '__main__':
    uw = UserWrangler()
    df = uw.get_pair_info(['BERZ', 'FNGD'])
    print(df)