from PairTrading.frontend.charting import DashChart
from PairTrading.backend.scanner import Scanner
from PairTrading.frontend.data_utils import DataUtils as du
from PairTrading.frontend.ui_pairview import PairView
from PairTrading.backend.data_wrangler import DataWrangler

from dash import Dash, html, dcc, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
import json


dw = DataWrangler()
scanner = Scanner()
scanner.min_price = 20
scanner.max_price = 170
scanner.min_avg_vol = 20000

ppairs = scanner.potential_pair
print(ppairs)
#print(ppair[ppair.potential_pair > 1].reset_index()) #GOLD AND SILVER ORES

#count = ppairs.set_index("industry")#.to_dict() #.get("GOLD AND SILVER ORES")
#count = ppairs[ppairs["industry"] == "FORESTRY"].potential_pair.iloc[0]
industry = "STATE COMMERCIAL BANKS"
industry_df = ppairs[ppairs["industry"] == industry]

if industry_df.empty:
    print("Empty")
else:
    print(industry_df.get("potential_pair").iloc[0])


#count = ppairs
#print(type(count))
#print(count)

#print(scanner.potential_pair_amount)