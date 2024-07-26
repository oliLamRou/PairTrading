import os
import time
import pandas as pd
import numpy as np
# from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.backend.scanner import Scanner
import math
import matplotlib.pyplot as plt
import itertools
import yfinance as yf
import pandas_ta
import sqlite3

# df = pd.read_csv('backend/wrangler/yahoo.csv')

# columns = tuple(df.columns.to_list())
# print("?, ".join(columns))
# # [tuple(row.to_list()) for i, row in df.iterrows()]


x = {'date', 'Ticker', 'adj_close', 'close', 'high', 'low', 'open', 'volume', 'timespan'}

print()