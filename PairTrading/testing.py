import pandas as pd
from PairTrading.backend.polygon import Polygon


p = Polygon()
print(p.get_table('ticker_details'))