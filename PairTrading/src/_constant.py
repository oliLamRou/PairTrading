from PairTrading.src.utils import PROJECT_ROOT

CONFIG = (PROJECT_ROOT / '.config.ini').resolve()

PAIR_INFO_COLUMNS = {
    'pair': ['pair', 'TEXT'],
    'A': ['A', 'TEXT'],
    'B': ['B', 'TEXT'],
    'reverse': ['reverse', 'INTERGER'],  
    'watchlist': ['watchlist', 'INTERGER'],
    'hedge_ratio': ['hedge_ratio', 'REAL'],
    'notes': ['notes', 'TEXT']
}

TICKER_RANK_COLUMNS = {
    'ticker': ['ticker', 'TEXT'],
    'rank': ['rank', 'INTERGER']
}

FAILED_TICKER_COLUMNS = {
    'ticker': ['ticker', 'TEXT'],
    'reformat': ['reformat', 'TEXT'],
}

MARKET_DATA_COLUMNS = {
    'ticker': ['ticker', 'TEXT'],
    'timespan': ['timespan', 'TEXT'],
    'Date': ['date', 'TEXT'],
    'Open': ['open', 'REAL'],
    'High': ['high', 'REAL'],
    'Low': ['low', 'REAL'],
    'Close': ['close', 'REAL'],
    'Adj Close': ['adj_close', 'REAL'],
    'Volume': ['volume', 'INTERGER'],
}

SIC_CODE_COLUMNS = {
    'sic_code': 'INTERGER',
    'office': 'TEXT',
    'industry_title': 'TEXT' 
}

GROUPED_DAILY_COLUMNS = {
    'T': ['ticker', 'TEXT'], 
    'v': ['volume', 'INTERGER'], 
    'vw': ['volume_weighted', 'REAL'], 
    'o': ['open', 'REAL'], 
    'c': ['close', 'REAL'], 
    'h': ['high', 'REAL'], 
    'l': ['low', 'REAL'], 
    't': ['timestamp', 'INTERGER'], 
    'n': ['n_transaction', 'INTERGER'],
    'otc': ['otc', 'INTERGER']
}

AGGREGATES_COLUMNS = {
    'c': ['close', 'REAL'],
    'h': ['high', 'REAL'],
    'l': ['low', 'REAL'],
    'n': ['n_transaction', 'INTERGER'],
    'o': ['open', 'REAL'],
    't': ['timestamp', 'INTERGER'],
    'v': ['volume', 'INTERGER'],
    'vw': ['volume_weighted', 'REAL'],
    'otc': ['otc', 'INTERGER']
}

TICKER_DETAILS_COLUMNS = {
    'ticker': ['ticker', 'TEXT'],
    'ticker_suffix': ['ticker_suffix', 'TEXT'],
    'name': ['name', 'TEXT'], 
    'market': ['market', 'TEXT'], 
    'locale': ['locale', 'TEXT'], 
    'primary_exchange': ['primary_exchange', 'TEXT'], 
    'type': ['type', 'TEXT'], 
    'active': ['active', 'INTERGER'], 
    'currency_name': ['currency_name', 'TEXT'], 
    'cik': ['cik', 'INTERGER'], 
    'composite_figi': ['composite_figi', 'TEXT'], 
    'share_class_figi': ['share_class_figi', 'TEXT'], 
    'market_cap': ['market_cap', 'REAL'], 
    'phone_number': ['phone_number', 'TEXT'], 
    'address': ['address', 'TEXT'], 
    'description': ['description', 'TEXT'],
    'sic_code': ['sic_code', 'INTERGER'], 
    'sic_description': ['sic_description', 'TEXT'], 
    'ticker_root': ['ticker_root', 'TEXT'], 
    'homepage_url': ['homepage_url', 'TEXT'], 
    'total_employees': ['total_employees', 'INTERGER'], 
    'list_date': ['list_date', 'TEXT'], 
    'branding': ['branding', 'TEXT'], 
    'share_class_shares_outstanding': ['share_class_shares_outstanding', 'INTERGER'], 
    'weighted_shares_outstanding': ['weighted_shares_outstanding', 'INTERGER'], 
    'round_lot': ['round_lot', 'INTERGER'],
    'is_test': ['is_test', 'INTERGER']
}

TICKER_TYPES_COLUMNS = {
    'code': ['code', 'TEXT'], 
    'description': ['description', 'TEXT'], 
    'asset_class': ['asset_class', 'TEXT'], 
    'locale': ['locale', 'TEXT']
}