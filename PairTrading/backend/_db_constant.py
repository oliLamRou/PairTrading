from PairTrading.src.utils import PROJECT_ROOT

POLYGON_DB = (PROJECT_ROOT / 'data' / 'polygon.db').resolve()
YFINANCE_DB = (PROJECT_ROOT / 'data' / 'local' / 'yfinance.db').resolve()
USER_DB = (PROJECT_ROOT / 'data' / 'local' / 'user.db').resolve()

#User
TICKER_RANK_TABLE_NAME = 'ticker_rank'
PAIR_INFO_TABLE_NAME = 'pair_info'

#Yahoo
MARKET_DATA_TABLE_NAME = 'market_data'
FAILED_TICKER_TABLE_NAME = 'failed_ticker'

#Polygon
TICKER_INFO_TABLE_NAME = 'ticker_details'
MARKET_SNAPSHOT_TABLE_NAME = 'grouped_daily'
SIC_CODE_TABLE_NAME = 'sic_code'
TICKER_TYPES_TABLE_NAME = 'ticker_types'