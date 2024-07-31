from PairTrading.backend.polygon import Polygon
from PairTrading.backend.data_wrangler import DataWrangler
import pandas as pd
from datetime import date

class DataUtils():
    @staticmethod
    def list_watchlist() -> list:
        watchlist = DataWrangler()._UserWrangler__user_db.get_table('watchlist')
        return watchlist.watchlist.to_list()

    @staticmethod
    def get_position(tickers: list) -> float:
        pass

    @staticmethod
    def get_average(ticker: str, column_name: str, period=30) -> float:
        return DataWrangler().market_data([ticker])[column_name].rolling(period).mean().to_list()[-1]
    
    @staticmethod
    def get_average_volume(ticker: str, period=30, market_data=pd.DataFrame()) -> float:
        if market_data.empty:
            return DataWrangler().market_data([ticker]).volume.rolling(period).mean().to_list()[-1]
        
        return market_data[market_data["ticker"] == ticker].volume.rolling(period).mean().to_list()[-1]
    
    @staticmethod
    def get_last_price(ticker, period="day", market_data=pd.DataFrame()) -> float:
        #NOTE: Should we cut today directly in datawrangler?
        if market_data.empty:
            today = pd.to_datetime(date.today())
            df = DataWrangler().market_data([ticker])
            df = df[(df.date != today)]
            return df[df.date == df.date.max()].close.iloc[0]

        df = market_data[market_data["ticker"] == ticker]
        return df[df.date == df.date.max()].close.iloc[0]
    
    @staticmethod
    def normalize_max(data: pd.Series()) -> pd.Series():
        return data / data.max()
    
    @staticmethod
    def normalize_minmax(data: pd.Series()) -> pd.Series():
        return (data - data.min()) / (data.max() - data.min())
    
    @staticmethod
    def format_large_number(num):
        suffixes = ['', 'K', 'M', 'B', 'T']
        magnitude = 0

        while abs(num) >= 1000 and magnitude < len(suffixes) - 1:
            magnitude += 1
            num /= 1000.0

        formatted_num = f"{num:.1f}{suffixes[magnitude]}"
        return formatted_num
        
if __name__ == '__main__':
    print(DataUtils.get_last_price('wec'))