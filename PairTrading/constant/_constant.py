GROUPED_DAILY_COLUMNS = {
    'symbol': 'TEXT', 
    'volume': 'INTERGER', 
    'volume_weighted': 'REAL', 
    'open': 'REAL', 
    'close': 'REAL', 
    'high': 'REAL', 
    'low': 'REAL', 
    'timestamp': 'INTERGER', 
    'n_transaction': 'INTERGER'
}

HISTORICAL_COLUMNS = {
    'c': ['close', 'REAL'],
    'h': ['high', 'REAL'],
    'l': ['low', 'REAL'],
    'n': ['n_transaction', 'INTERGER'],
    'o': ['open', 'REAL'],
    't': ['timestamp', 'INTERGER'],
    'v': ['volume', 'INTERGER'],
    'vw': ['volume_weighted', 'REAL']
}

TICKER_DETAILS_COLUMNS = {
    'ticker': 'TEXT',
    'ticker_suffix': 'TEXT',
    'name': 'TEXT', 
    'market': 'TEXT', 
    'locale': 'TEXT', 
    'primary_exchange': 'TEXT', 
    'type': 'TEXT', 
    'active': 'INTERGER', 
    'currency_name': 'TEXT', 
    'cik': 'INTERGER', 
    'composite_figi': 'TEXT', 
    'share_class_figi': 'TEXT', 
    'market_cap': 'REAL', 
    'phone_number': 'TEXT', 
    'address': 'TEXT', 
    'description': 'TEXT',
    'sic_code': 'INTERGER', 
    'sic_description': 'TEXT', 
    'ticker_root': 'TEXT', 
    'homepage_url': 'TEXT', 
    'total_employees': 'INTERGER', 
    'list_date': 'TEXT', 
    'branding': 'TEXT', 
    'share_class_shares_outstanding': 'INTERGER', 
    'weighted_shares_outstanding': 'INTERGER', 
    'round_lot': 'INTERGER'
}