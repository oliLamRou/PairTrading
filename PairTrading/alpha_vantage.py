import pandas as pd
import requests
import configparser
import io
import os
import random

# url = f'https://www.alphavantage.co/query?function={interval}&symbol={symbol}&apikey={key}&datatype={datatype}'

# r = requests.get(url).content
# c = pd.read_csv(io.StringIO(r.decode('utf-8')))
# c.to_csv('../data/symbol.csv', index=False)


class AlphaVantage:
	ALL_SYMBOLS_PATH = '../data/all_symbol.csv'

	def __init__(self):
		self.config = configparser.ConfigParser()
		self.config.read('../.config.ini')

		#Key
		self.key = self.config['alpha_vantage']['API_KEY']

		self.base_url = 'https://www.alphavantage.co/query?'
		self.all_symbols = []

	def daily(self, symbol):
		outputsize = 'compact'
		interval = 'TIME_SERIES_DAILY'
		datatype = 'csv'

		url = f'{self.base_url}function={interval}&symbol={symbol}&apikey={self.key}&datatype={datatype}'
		r = requests.get(url).content
		df = pd.read_csv(io.StringIO(r.decode('utf-8')))
		df.to_csv(f'../data/{symbol}.csv', index=False)	

		print(df)

	def symbols(self, refresh=False):
		if refresh:
			url = f'{self.base_url}function=LISTING_STATUS&apikey={self.key}&state=active'
			r = requests.get(url).content
			df = pd.read_csv(io.StringIO(r.decode('utf-8')))
			df.to_csv(self.ALL_SYMBOLS_PATH, index=False)

		df = pd.read_csv(self.ALL_SYMBOLS_PATH)
		print(df.info())

		print('Exchanges:', df.exchange.unique())
		print('Asset Type:', df.assetType.unique())
		self.all_symbols = df.symbol.to_list()

		# print(df[df.exchange == 'NYSE'].symbol.to_list())



if __name__ == '__main__':
	av = AlphaVantage()
	av.symbols()
	symbols = av.all_symbols
	random.shuffle(symbols)
	for symbol in symbols:
		if os.path.exists(f'../data/{symbol}.csv'):
			continue

		av.daily(symbol)