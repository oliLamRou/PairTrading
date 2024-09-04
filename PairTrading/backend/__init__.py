from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from PairTrading.backend.models import PolygonBase, UserBase, YahooBase

PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG = (PROJECT_ROOT / '.config.ini').resolve()

#Polygon
POLYGON_DB = (PROJECT_ROOT / 'data' / 'polygon.db').resolve()
polygon_engine = create_engine(f'sqlite:///{POLYGON_DB}', echo = False)
PolygonBase.metadata.create_all(polygon_engine)
PolygonSession = sessionmaker(bind = polygon_engine)
polygon_session = PolygonSession()

#User
USER_DB = (PROJECT_ROOT / 'data' / 'local' / 'user.db').resolve()
user_engine = create_engine(f'sqlite:///{USER_DB}', echo = False)
UserBase.metadata.create_all(user_engine)
UserSession = sessionmaker(bind = user_engine)
user_session = UserSession()

#User
YAHOO_DB = (PROJECT_ROOT / 'data' / 'local' / 'yfinance.db').resolve()
yahoo_engine = create_engine(f'sqlite:///{YAHOO_DB}', echo = False)
YahooBase.metadata.create_all(yahoo_engine)
YahooSession = sessionmaker(bind = yahoo_engine)
yahoo_session = YahooSession()

