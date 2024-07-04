from PairTrading.frontend.charting import DashChart
from PairTrading.backend.polygon import Polygon
from PairTrading.frontend.data_utils import DataUtils
from PairTrading.frontend.pair import Pair

from PairTrading.src import _constant
import pandas as pd

from dash import Dash, html, dcc, Input, Output  # pip install dash
import dash_bootstrap_components as dbc   # pip install dash-bootstrap-components

p = Polygon()
dataKeys = {
    "Time" : _constant.HISTORICAL_COLUMNS['t'][0], 
    "Open" : _constant.HISTORICAL_COLUMNS['o'][0],
    "Close" : _constant.HISTORICAL_COLUMNS['c'][0], 
    "High" : _constant.HISTORICAL_COLUMNS['h'][0], 
    "Low" : _constant.HISTORICAL_COLUMNS['l'][0]
}

#tickers = ["day_AA", "day_MSTR", "day_AU", "day_CMA", "day_DVN", "day_GCT", "day_AZEK", "day_BTI", "day_CFLT"]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
d = DataUtils()
pair = Pair(["AA", "AU"])
pair.calculate_order()

df = p.get_table("day_AA")
cdf = p.get_table("day_AU")

chart_compare = DashChart("A/B Compare", "compare")
chart_compare.data = df
chart_compare.compareData = cdf
chart_compare.dataKeys = dataKeys
chart_compare.set_callback_app(app)

chart_ratio = DashChart("Pair Ratio", "line")
ddf = pd.DataFrame()
ddf['timestamp'] = df.timestamp
ddf['close'] = df.close / cdf.close
chart_ratio.data = ddf
chart_ratio.dataKeys = dataKeys
chart_ratio.set_callback_app(app)

chart_pairPrice = DashChart("Pair Price", "candlestick")
chart_pairPrice.data = df
chart_pairPrice.compareData = cdf
chart_pairPrice.dataKeys = dataKeys
chart_pairPrice.set_callback_app(app)

layout_objects = []
    
#pair details card
pairDetailsCard = [
    html.H3("Pair A / B", className="card-title"),
    html.Div(d.get_last_price("AA"))
]

#pair view card
pairViewCard = [
    dbc.CardHeader(html.H3("Pair A / B", className="card-title")),
    dbc.CardBody([
        dbc.Row([
            #charts
            dbc.Col([
                dbc.Row(dbc.Col(chart_pairPrice.get_layout())),
                dbc.Row([
                    dbc.Col(chart_compare.get_layout(),width=6),
                    dbc.Col(chart_ratio.get_layout(),width=6),
                ])
            ], width="8"),
            #details
            dbc.Col(
                dbc.Row(dbc.Col(pairDetailsCard))
            )
        ])
    ])
]

chartCard = dbc.Card(
    pairViewCard
)        
                
layoutElements = [
    chartCard
]

app.layout = html.Div(
    layoutElements,
)
app.run_server(debug=True, port=8060)
