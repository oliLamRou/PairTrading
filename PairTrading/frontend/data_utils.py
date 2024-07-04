from PairTrading.backend.polygon import Polygon
from PairTrading.backend.data_wrangler import DataWrangler
import pandas as pd

class DataUtils():
    def __init__(self):
        self.dw = DataWrangler()
    
    def get_ticker_details(self, ticker=""):
        df = self.dw.market_data("ticker")
        return df
    
    def get_ticker_data(self, ticker, data=""):
        return self.dw.ticker_info(ticker)
    
    def get_average_volume(self, ticker="", period=30):
        v = self.get_ticker_details(ticker).volume[-period:].mean()
        return v
    
    def get_last_price(self, ticker="", period="day"):
        v = self.get_ticker_details(ticker).close[-1:]
        return v
    
    def normalize_max(self, df, column=""):
        ddf = df.copy()
        ddf[column] = df[column] / df[column].max()
        return ddf
    
    def normalize_minmax(self, df, column=""):
        ddf = df.copy()
        ddf[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
        return ddf
        
if __name__ == '__main__':
    d = DataUtils()
    #print(d.p.grouped_daily("day_AA"))
    #df = d.get_ticker_data("")
    #nrm = d.normalize_max(df, "close")
    #print(nrm)
    #print(d.normalize_minmax(df, "close"))

    #print(d.get_average_volume("AA", 30))
    #print(d.get_last_price("AA"))