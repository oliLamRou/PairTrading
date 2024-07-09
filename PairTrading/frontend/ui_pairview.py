from PairTrading.frontend.charting import DashChart
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.frontend.data_utils import DataUtils
from PairTrading.frontend.pair import Pair

from PairTrading.src import _constant
import pandas as pd
from dash import Dash, html, dcc, Input, Output 
import dash_bootstrap_components as dbc  

class PairView:
    def __init__(self):
        self.test = "wtf"
        self.dw = DataWrangler()
        self.d = DataUtils()
        self.df = self.dw.market_data("AA")
        self.cdf = self.dw.market_data("AU")
        self.app = None

        self.layout_elements=[]

    def set_callback_app(self, app):
        self.app = app
        
    def build(self):
        print("build")

        chart_compare = DashChart("A/B Compare", "compare")
        chart_compare.data = self.df
        chart_compare.compareData = self.cdf
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

if __name__ == '__main__':
    print("damn")