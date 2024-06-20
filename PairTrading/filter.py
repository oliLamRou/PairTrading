import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from PairTrading.polygon import Polygon


class Filter(Polygon):
	def __init__(self):
		super().__init__()

def get_avg(stock):
	print(stock)
	close = pd.read_csv(f'../data/historical/{stock}.csv')['c']
	min_val = close.min()
	max_val = close.max()
	normalized = ((close - min_val) / (max_val - min_val)).mean().round(2)
	return normalized


stocks = []
for filename in os.listdir('../data/historical'):
	symbol = '.'.join(filename.split('.')[:-1])
	df = pd.read_csv(f'../data/historical/{symbol}.csv')
	if df.c.iloc[-1] < 20 or df.c.iloc[-1] > 120:
		continue

	if df.v[-30:].mean() < 500000 or df.v[-30:].mean() > 5000000:
		continue

	stocks.append(symbol)

# stocks = [file.split('.')[0] for file in os.listdir('../data/stocks')]
stocks.sort()
stocks = stocks[:10]

avg = [get_avg(stock) for stock in stocks]
avg_array = np.array(avg)

# Calculate the difference using broadcasting
diff_matrix = avg_array[:, np.newaxis] - avg_array

# Convert the result back to a DataFrame if desired
df = pd.DataFrame(diff_matrix, columns=stocks, index=stocks)

plt.figure(figsize=(10, 10))
# heatmap = sns.heatmap(df, cmap='coolwarm')
# plt.savefig('./heatmap.jpeg', format='jpeg', dpi=100)
# plt.show()

stock1 = pd.read_csv('../data/historical/AA.csv')
stock2 = pd.read_csv('../data/historical/AAAU.csv')

df = stock1[['t', 'c']].merge(stock2[['t', 'c']], on='t', suffixes=['_AA', '_AAAU'])
df.set_index('t', inplace=True)
line = sns.lineplot(data=df)
plt.show()


#Get recent data
#Get sector list
#mosaic pair chart