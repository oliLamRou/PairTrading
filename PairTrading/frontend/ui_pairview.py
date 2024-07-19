from PairTrading.frontend.charting import DashChart
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.frontend.pair import Pair

import pandas as pd
from dash import Dash, html, dcc, Input, Output 
import dash_bootstrap_components as dbc  

class PairView:
    def __init__(self, ticker_a, ticker_b, diff_average=1, ratio=1, show_header=True):
        self.ticker_a = ticker_a
        self.ticker_b = ticker_b
        self.show_header = show_header
        self.ratio = 0.61
        self.diff_average = diff_average
        self.market_data = None
        self.callback_app = None

        #Pair Price Chart
        self.chart_pairPrice = DashChart(f"{self.ticker_a}-{self.ticker_b}-price-chart", "candlestick")
        self.chart_pairPrice.label = "Pair Price"

        #Pair Compare Chart
        self.chart_compare = DashChart(f"{self.ticker_a}-{self.ticker_b}-Compare-chart", "compare")
        self.chart_compare.label = "Pair Compare"

        #Pair Ratio Chart
        self.chart_ratio = DashChart(f"{self.ticker_a}-{self.ticker_b}-ratio-chart", "line")
        self.chart_ratio.label = "Pair Ratio"
        
    def set_callback_app(self, app):
        self.callback_app = app
        self.chart_pairPrice.set_callback_app(self.callback_app)
        self.chart_compare.set_callback_app(self.callback_app)
        self.chart_ratio.set_callback_app(self.callback_app)
        
    def build(self):
        print("build")

    def get_layout(self):
        
        df_a = self.market_data[self.market_data.ticker == self.ticker_a]
        df_b = self.market_data[self.market_data.ticker == self.ticker_b]
        #print(df_a)

        ddf = pd.DataFrame()

        ddf['date'] = df_a.index
        ddf['close'] = df_a.close - df_b.close * self.ratio
        
        #Pair Price Chart
        self.chart_pairPrice.data = df_a
        self.chart_pairPrice.compareData = ddf

        #Pair Compare Chart
        self.chart_compare.data = df_a
        self.chart_compare.compareData = df_b

        #Pair Ratio Chart
        ratio_df = (df_a.set_index("date").close / df_b.set_index("date").close).reset_index()
        self.chart_ratio.data = ratio_df

        #pair details card
        detail_card = [
            dbc.Card([
                dbc.CardHeader(html.H4(f"{self.ticker_a}-{self.ticker_b} Details", className="card-title")),
                dbc.CardBody([
                    #html.H3("Pair Details", className="card-title"),
                    html.Div([
                        html.P("Pair Price: xxxx"),
                        html.P(f"{self.ticker_a} Dollar Volume Average: "),
                        html.P(f"{self.ticker_b} Dollar Volume Average: "),
                        html.Br(),
                        dbc.Checklist(options=[{"label": "Watchlist", "value": 1},{"label": "Reverse Order", "value": 2},],value=[],id="switches-input",inline=False,switch=True,),
                        dbc.InputGroup([dbc.InputGroupText("Hedge Ratio"), dbc.Input(placeholder="Ratio", type="number", step=0.01)], className="mb-3"),
                        dbc.InputGroup([dbc.InputGroupText("Notes"), dbc.Textarea()], className="mb-3"),
                        #html.P(f"Pair Last Price: {df_a.iloc[-1:].close.unique()[0]}") ,
                        
                        
                        dbc.Button("Reset", color="primary", disabled=True),
                        dbc.Button("Save", color="primary", disabled=True),
                    ])              
                ])
            ])
        ]

        #pair view card
        chart_card = [
            #dbc.CardHeader(html.H3(f"{self.ticker_a}-{self.ticker_b} Pair", className="card-title")),
            #dbc.CardHeader(html.H3(dbc.InputGroup([dbc.InputGroupText("Tickers: "), dbc.Input(id="pair-tickers", type="text", value="LNT, WEC")]))),
            #dbc.CardBody([
                dbc.Row([
                    #charts
                    dbc.Col([
                        dbc.Row(dbc.Col(self.chart_pairPrice.get_layout())),
                        dbc.Row([
                            dbc.Col(self.chart_compare.get_layout(),width=6),
                            dbc.Col(self.chart_ratio.get_layout(),width=6),
                        ])
                    ], width="8"),

                    #details
                    dbc.Col(
                        dbc.Row(dbc.Col(detail_card))
                    )
                ])
            #])
        ]
       
        layout_elements = [
            #dbc.Card(chart_card)
            html.Div(chart_card)
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