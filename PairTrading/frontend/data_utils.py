from PairTrading.backend.polygon import Polygon
from PairTrading.backend.data_wrangler import DataWrangler
import pandas as pd
from datetime import date

class DataUtils():
    @staticmethod
    def get_average(ticker: str, column_name: str, period=30) -> float:
        return DataWrangler().market_data([ticker])[column_name].rolling(period).mean().to_list()[-1]
    
    @staticmethod
    def get_average_volume(ticker: str, period=30) -> float:
        return DataWrangler().market_data([ticker]).volume.rolling(period).mean().to_list()[-1]
    
    @staticmethod
    def get_last_price(ticker, period="day") -> float:
        #NOTE: Should we cut today directly in datawrangler?
        today = pd.to_datetime(date.today())
        df = DataWrangler().market_data([ticker])
        return df[df.date != today].max().close
    
    @staticmethod
    def normalize_max(data: pd.Series()) -> pd.Series():
        return data / data.max()
    
    @staticmethod
    def normalize_minmax(data: pd.Series()) -> pd.Series():
        return (data - data.min()) / (data.max() - data.min())
        
if __name__ == '__main__':
    print('Avg Price:', DataUtils.get_average('AAPL', 'close'))
    print('Avg Vol:', DataUtils.get_average_volume('AAPL'))
    print('Last Close:', DataUtils.get_last_price('AAPL'))

    dw = DataWrangler()
    df = dw.market_data(['AAPL'])
    print('Normalize Max:', DataUtils.normalize_max(df.close).tail(5))
    print('Normalize MinMax:', DataUtils.normalize_minmax(df.close).tail(5))

    #Exemple
    df['NM'] = DataUtils.normalize_max(df.close)