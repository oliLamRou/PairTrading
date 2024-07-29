from PairTrading.frontend.charting import DashChart
from PairTrading.backend.scanner import Scanner
from PairTrading.frontend.data_utils import DataUtils as du
from PairTrading.frontend.ui_pairview import PairView
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.backend.ibkr import IBUtils as ib

from dash import Dash, html, dcc, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
import json
import pandas as pd

scanner = Scanner()
df = scanner.market_data("CMAX")
print(df)
print("test")
print(ib.get_trades("CMAX"))

# data = [{"test1" : 1, "test2" : 2}, {"test1" : 34, "test2" : 9999}]
# df = pd.DataFrame(data=data)
# print(df.to_dict())