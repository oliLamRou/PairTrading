import time
import pandas as pd
import sqlite3
from PairTrading.database import DataBase
from PairTrading.polygon import Polygon
import os

p = Polygon()
# print(p.list_tables())
print(p.get_table('ticker_details'))
# for file in os.listdir('../data/historical'):
# 	df = pd.read_csv(f'../data/historical/{file}')
# 	ticker = file.split('.')[0]
# 	t = p.list_tables()
# 	if f'day_{ticker}' in [x[0] for x in t]:
# 		print('skipping', ticker)
# 		continue

# 	results = []
# 	for i, row in df.iterrows():
# 		results.append({
# 			'c': row.c,
# 			'h': row.h,
# 			'l': row.l,
# 			'n': row.n,
# 			'o': row.o,
# 			't': row.t,
# 			'v': row.v,
# 			'vw': row.vw,
# 		})

# 	p.historical_(ticker, results)
# 	time.sleep(2)
# 	print(p.get_table(f'day_{ticker}'))