import time
import pandas as pd
import numpy as np
from PairTrading.backend.data_wrangler import DataWrangler
import math
import matplotlib.pyplot as plt
import itertools

dw = DataWrangler()

df = dw.all_market_data()

# print(df.ticker)


# df_pivot = df.pivot(index='date', columns='ticker', values='close')
df_ = df.pivot(index='timestamp', columns='ticker', values='close')
print((df_['AA'] - df_['AAAU']).mean())

x = [1,2,3,4]
a = itertools.combinations(x, 2)

print(list(a))