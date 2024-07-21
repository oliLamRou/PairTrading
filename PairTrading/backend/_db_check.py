from PairTrading.backend.scanner import Scanner
from PairTrading.backend.scanner import Scanner


def update_ticker_info(self):
    self.min_price = 2
    self.max_price = 200
    self.min_vol = 100
    tickers = self.snapshot_filter
    for ticker in tickers:
        if not self._DataWrangler__polygon_db.has_value('ticker_details', 'ticker', ticker):
            print(f'/// Doing {ticker}')
            df = self.ticker_info(ticker)
            missing = set(tickers).difference(set(self._DataWrangler__polygon_db.get_table('ticker_details').ticker.to_list()))
            print(f'-> {len(missing)} to download\n')
            time.sleep(13)
        else:
            print('DONE:', ticker)

s = Scanner()

def polygon(update_snapshot=False, update_ticker_info=False):
	#Polygon
	polygon_tables = s._DataWrangler__polygon_db.list_tables()

	for table_name in polygon_tables.name.to_list():
		df = s._DataWrangler__polygon_db.get_table(table_name)
		print(
			f'-> {table_name} head\n',
			df.columns.to_list(), '\n',
	        df.head(),
			'\n'
		)

def yahoo():
	yf_tables = s._DataWrangler__yfinance_db.list_tables()
	print('Yahoo Tables:\n', yf_tables, '\n')

	#Market Data
	md = s.all_market_data
	print(
		'-> Market Data Sample\n',
		f'{len(md.ticker.unique())} tickers\n',
		f'Timespans: {md.timespan.unique()}\n',
		md.sample(5),
		'\n'
	)

def user():
	#User
	user_tables = s._DataWrangler__user_db.list_tables()
	print('User Tables:\n', user_tables, '\n')

	for table_name in user_tables.name.to_list():
		df = s._DataWrangler__user_db.get_table(table_name)
		print(
			f'-> {table_name} head\n',
			df.columns.to_list(), '\n',
	        s._DataWrangler__user_db.get_table(table_name).head(),
			'\n'
		)

polygon()
yahoo()
user()