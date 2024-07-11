from PairTrading.frontend.charting import DashChart
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.frontend.pair import Pair

import pandas as pd
from dash import Dash, html, dcc, Input, Output 
import dash_bootstrap_components as dbc  

class PairView:
    def __init__(self, ticker_a, ticker_b, diff_average=1, ratio=1):
        self.ticker_a = ticker_a
        self.ticker_b = ticker_b
        self.ratio = 0.61
        self.diff_average = diff_average
        self.market_data = None
        self.callback_app = None

    def set_callback_app(self, app):
        self.callback_app = app
        
    def build(self):
        print("build")

    def get_layout(self):
        df_a = self.market_data[self.market_data.ticker == self.ticker_a]
        df_b = self.market_data[self.market_data.ticker == self.ticker_b]

        ddf = pd.DataFrame()

        ddf['date'] = df_a.index
        ddf['close'] = df_a.close - df_b.close * self.ratio
        
        #Pair Price Chart
        chart_pairPrice = DashChart("price chart", "candlestick")
        chart_pairPrice.label = "Pair Price"
        chart_pairPrice.data = df_a
        chart_pairPrice.compareData = ddf
        chart_pairPrice.set_callback_app(self.callback_app)

        #Pair Compare Chart
        chart_compare = DashChart("Compare-chart", "compare")
        chart_compare.label = "Pair Compare"
        chart_compare.data = df_a
        chart_compare.compareData = df_b
        chart_compare.set_callback_app(self.callback_app)

        #Pair Ratio Chart
        ratio_df = (df_a.set_index("date").close / df_b.set_index("date").close).reset_index()
        chart_ratio = DashChart("ratio-chart", "line")
        chart_ratio.label = "Pair Ratio"
        chart_ratio.data = ratio_df
        chart_ratio.set_callback_app(self.callback_app)

        #pair details card
        detail_card = [
            dbc.Card([
                dbc.CardHeader(html.H4(f"{self.ticker_a}-{self.ticker_b} Details", className="card-title")),
                dbc.CardBody([
                    #html.H3("Pair Details", className="card-title"),
                    html.Div([
                        html.P("Pair Order"),
                        html.P(f"Pair Last Price: {df_a.iloc[-1:].close.unique()[0]}") ,
                        html.P(f"{self.ticker_a} Dollar Volume Average: "),
                        html.P(f"{self.ticker_b} Dollar Volume Average: ")
                    ])              
                ])
            ])
        ]

        #pair view card
        chart_card = [
            #dbc.CardHeader(html.H3(f"{self.ticker_a}-{self.ticker_b} Pair", className="card-title")),
            dbc.CardHeader(html.H3(dbc.InputGroup([dbc.InputGroupText("Tickers: "), dbc.Input(id="pair-tickers", type="text", value="LNT, WEC")]))),
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
                        dbc.Row(dbc.Col(detail_card))
                    )
                ])
            ])
        ]
       
        layout_elements = [
            dbc.Card(chart_card)
        ]

        return layout_elements

if __name__ == '__main__':
    print("ui_pairview")
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    dw = DataWrangler()
    df = dw.all_market_data

    pair_view = PairView("LNT", "WEC")
    pair_view.market_data = df
    pair_view.set_callback_app(app)

    app.layout = html.Div(
        pair_view.get_layout()
    )

    app.run_server(debug=True, port=8060)