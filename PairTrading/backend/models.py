from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, synonym

PolygonBase = declarative_base()
YahooBase = declarative_base()
UserBase = declarative_base()

class SicCode(PolygonBase):
    __tablename__ = 'sic_code'
    id = Column(Integer, primary_key = True, autoincrement=True)

    SicCode                         = Column('sic_code', Integer)
    sic_code                        = synonym('SicCode')

    Office                          = Column('office', String)
    office                          = synonym('Office')

    IndustryTitle                   = Column('industry_title', String)
    industry_title                  = synonym('IndustryTitle')

class TickerDetails(PolygonBase):
    __tablename__ = 'ticker_details'
    id = Column(Integer, primary_key = True, autoincrement=True)

    ticker                          = Column(String)
    ticker_suffix                   = Column(String)
    name                            = Column(String)
    market                          = Column(String)
    locale                          = Column(String)
    primary_exchange                = Column(String)
    type                            = Column(String)
    active                          = Column(Integer)
    currency_name                   = Column(String)
    cik                             = Column(Integer)
    composite_figi                  = Column(String)
    share_class_figi                = Column(String)
    market_cap                      = Column(Float)
    phone_number                    = Column(String)
    address                         = Column(String)
    description                     = Column(String)
    sic_code                        = Column(Integer)
    sic_description                 = Column(String)
    ticker_root                     = Column(String)
    homepage_url                    = Column(String)
    total_employees                 = Column(Integer)
    list_date                       = Column(String)
    branding                        = Column(String)
    share_class_shares_outstanding  = Column(Integer)
    weighted_shares_outstanding     = Column(Integer)
    round_lot                       = Column(Integer)
    is_test                         = Column(Integer)


class MarketSnapshot(PolygonBase):
    __tablename__ = 'market_snapshot'
    id = Column(Integer, primary_key = True, autoincrement=True)

    T               = Column('ticker', String)
    Ticker          = synonym('Ticker')

    v               = Column('volume', Integer)
    Volume          = synonym('Volume')

    vw              = Column('volume_weighted', Float)
    VolumeWeighted  = synonym('VolumeWeighted')

    o               = Column('open', Float)
    Open            = synonym('Open')
    
    c               = Column('close', Float)
    Close           = synonym('Close')

    h               = Column('high', Float)
    High            = synonym('High')

    l               = Column('low', Float)
    Low             = synonym('Low')

    t               = Column('timestamp', Integer)
    Timestamp       = synonym('Timestamp')

    n               = Column('n_transaction', Integer)
    NTransaction    = synonym('NTransaction')

    otc             = Column('otc', Integer)
    OTC             = synonym('OTC')

class MarketData(YahooBase):
    __tablename__ = 'market_data'
    id = Column(Integer, primary_key = True, autoincrement=True)

    Ticker      = Column('ticker', String)
    Timespan    = Column('timespan', Integer)
    Date        = Column('date', String)
    Open        = Column('open', Float)
    High        = Column('high', Float)
    Low         = Column('low', Float)
    Close       = Column('close', Float)
    AdjClose    = Column('adj_close', Float)
    Volume      = Column('volume', Integer)

class FailedTicker(YahooBase):
    __tablename__ = 'failed_ticker'
    id = Column(Integer, primary_key = True, autoincrement=True)

    Ticker      = Column('ticker', String)
    Reformat    = Column('reformat', String)

class PairInfo(UserBase):
    __tablename__ = 'pair_info'
    id = Column(Integer, primary_key = True, autoincrement=True)

    A           = Column('A',String)
    B           = Column('B', String)

    Pair        = Column('pair', String)
    pair        = synonym('Pair')
    
    Reverse     = Column('reverse', Integer)
    reverse     = synonym('Reverse')
    
    Watchlist   = Column('watchlist', Integer)
    watchlist   = synonym('Watchlist')    
    
    HedgeRatio  = Column('hedge_ratio', Float)
    hedge_ratio = synonym('HedgeRatio')
    
    Period      = Column('period', Integer)
    period      = synonym('Period')
    
    StdDev      = Column('std_dev', Integer)
    std_dev     = synonym('StdDev')
    
    Notes       = Column('notes', String)
    notes       = synonym('Notes')