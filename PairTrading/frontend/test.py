from PairTrading.backend.database import DataBase
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.src import _constant
from PairTrading.src.utils import PROJECT_ROOT
import pandas as pd

""" polygon_db_path = (PROJECT_ROOT / 'data' / 'polygon.db').resolve()
db = DataBase(path = polygon_db_path)
df = pd.DataFrame()
#df.items
df = db.list_tables()
#print(df)

tickers = []
print(df)
print(tickers)
 """

dw = DataWrangler()
df = dw.market_data("AA")
info = dw.ticker_info("AA")
print(info.sic_code)

dw = DataWrangler()
tickers = dw.market_snapshot().ticker

""" for t in tickers:
    print(t) """


