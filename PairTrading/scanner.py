from alpha_vantage.timeseries import TimeSeries
import pandas as pd

api_key = 'your_api_key'
ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_intraday(symbol='AAPL', interval='1min', outputsize='compact')
print(data.head())
