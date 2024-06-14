import pandas as pd
from PairTrading.backend.data import Data

d = Data()

df = d.get_aggregates('AAPL', update=False)

avg = df[-30:].volume.mean().astype(int)

print(avg)

get_grouped_daily   market_snapshot
get_ticker_details  ticker_info
get_ticker_types    
get_aggregates      market_data