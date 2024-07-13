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
	
	#Snapshot
	if update_snapshot:
		s.market_snapshot(update=True)

	print(
		'Polygon Tables:\n', 
		polygon_tables, 
		'\n')

	#Ticker Info
	if update_ticker_info:
		pass

	print(
		'-> Ticker Info Sample\n',
		s.all_ticker_info.sample(5),
		'\n'
	)

	#SIC Code
	print(
		'-> SIC Code Sample\n',
		s.sic_code.sample(5),
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

	#Ticker Rank
	print(
		'-> User Rank Sample\n',
        s._DataWrangler__user_db.get_table('ticker_rank'),
		'\n'
	)

polygon()
yahoo()
user()