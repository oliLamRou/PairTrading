import pandas as pd
import os

all_symbols = pd.read_csv('_all_symbol.csv')['symbol'].to_list()

for file in os.listdir('./Stocks/'):
	symbol = file.split('.')[0].upper()
	if not symbol in all_symbols:
		continue

	try:
		df = pd.read_csv(f'./Stocks/{file}', on_bad_lines='skip')
	except:
		print('skip:', file)
		continue

	df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

	df_2015 = df[(df['Date'].dt.year == 2015)]
	if df_2015.empty or len(df_2015.Date.dt.month.unique()) < 12:
		continue

	df_2016 = df[(df['Date'].dt.year == 2016)]
	if df_2016.empty or len(df_2016.Date.dt.month.unique()) < 12:
		continue

	df = pd.concat([df_2015, df_2016])
	df.to_csv(f'./{symbol}.csv', index=False)