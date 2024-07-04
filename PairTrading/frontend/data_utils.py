from PairTrading.backend.polygon import Polygon
import pandas as pd

class DataUtils():
    def __init__(self):
        self.p = Polygon()
    
    def get_ticker_details(self, ticker=""):
        df = self.p.get_table(f"day_{ticker}")
        return df
    
    def get_ticker_data(self, ticker, data=""):
        return []
    
    def get_average_volume(self, ticker="", period=30):
        v = self.get_ticker_details(ticker).volume[-period:].mean()
        return v
    
    def get_last_price(self, ticker="", period="day"):
        v = self.get_ticker_details(ticker).close[-1:].iloc[0]
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
    df = d.p.get_table("day_AA")
    nrm = d.normalize_max(df, "close")
    print(nrm)
    print(d.normalize_minmax(df, "close"))

    #print(d.get_average_volume("AA", 30))
    #print(d.get_last_price("AA"))