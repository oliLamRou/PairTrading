import pandas as pd
import requests
import configparser
import io

config = configparser.ConfigParser()
config.read('../.config.ini')

interval = 'TIME_SERIES_DAILY'
symbol = 'NVDA'
key = config['alpha_vantage']['API_KEY']
datatype = 'csv'

url = f'https://www.alphavantage.co/query?function={interval}&symbol={symbol}&apikey={key}&datatype={datatype}'

r = requests.get(url).content
c = pd.read_csv(io.StringIO(r.decode('utf-8')))
c.to_csv('../data/symbol.csv', index=False)

r = requests.get(f'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={key}').content
c = pd.read_csv(io.StringIO(r.decode('utf-8')))
c.to_csv('../data/all_symbol.csv', index=False)
