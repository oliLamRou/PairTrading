from PairTrading.frontend.charting import DashChart
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.frontend.pair import Pair
from PairTrading.frontend.data_utils import DataUtils as du
from PairTrading.backend.scanner import Scanner

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
        print(df_a)

        #ddf = df_a.copy()
        ddf = pd.DataFrame()

        #if not reverse:
        ddf = df_a.merge(df_b, on='date', suffixes=['_a', '_b'])
        #else:
        #   ddf = df_a.merge(df_b, on='date', suffixes=['_b', '_a'])

        ddf["open"] = ddf["open_a"] - ddf["open_b"] * self.ratio
        ddf["close"] = ddf["close_a"] - ddf["close_b"] * self.ratio
        ddf["high"] = ddf["high_a"] - ddf["high_b"] * self.ratio
        ddf["low"] = ddf["low_a"] - ddf["low_b"] * self.ratio

        #Pair Price Chart
        self.chart_pairPrice.data = ddf

        #Pair Compare Chart
        self.chart_compare.data = df_a
        self.chart_compare.compareData = df_b

        #Pair Ratio Chart
        ratio_df = (df_a.set_index("date").close / df_b.set_index("date").close).reset_index()
        self.chart_ratio.data = ratio_df

        #if reverse to swap with pair info data
        if True:
            pair_price = du.get_last_price(self.ticker_a) - (du.get_last_price(self.ticker_b) * self.ratio)
        else:
            pair_price = du.get_last_price(self.ticker_b) - (du.get_last_price(self.ticker_a) * self.ratio)

        detail_tab = html.Div([
            html.P(f"Pair Price: {pair_price}"),
            html.P("Average Difference: xxxx"),
            html.P(f"{self.ticker_a} Dollar Volume Average: "),
            html.P(f"{self.ticker_b} Dollar Volume Average: "),
            html.Br(),
            dbc.Checklist(options=[{"label": "Watchlist", "value": 1},{"label": "Reverse Order", "value": 2},],value=[],id="switches-input",inline=False,switch=True,),
            dbc.InputGroup([dbc.InputGroupText("Hedge Ratio"), dbc.Input(placeholder="Ratio", type="number", step=0.01, value=self.ratio)], className="mb-3"),
            dbc.InputGroup([dbc.InputGroupText("Notes"), dbc.Textarea()], className="mb-3"),
            #html.P(f"Pair Last Price: {df_a.iloc[-1:].close.unique()[0]}") ,
            
            
            dbc.Button("Reset", color="primary", disabled=True),
            dbc.Button("Save", color="primary", disabled=True),
        ], style={"margin" : "2%"})

        trades_tab = dbc.Card(
            dbc.CardBody(
                    "trades"
            ),
        )

        #pair details card

        detail_card = [
            dbc.Card([
                dbc.CardHeader(html.H4(f"{self.ticker_a}-{self.ticker_b} Details", className="card-title")),
                dbc.Tabs([
                    dbc.Tab(detail_tab, label="Details"),
                    dbc.Tab(trades_tab, label="Trades"),
                    #dbc.Tab("This tab's content is never seen", label="Tab 3", disabled=True),
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

    scanner=Scanner()
    scanner.min_price = 2
    scanner.max_price = 200
    scanner.min_vol = 100000

    df = scanner.market_data(["LNT", "WEC"])

    pair_view = PairView("LNT", "WEC")
    pair_view.market_data = df
    pair_view.set_callback_app(app)

    app.layout = html.Div(
        pair_view.get_layout()
    )

    app.run_server(debug=True, port=8060)