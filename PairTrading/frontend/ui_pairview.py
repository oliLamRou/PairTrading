from PairTrading.frontend.charting import DashChart
import time
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.frontend.pair import Pair
from PairTrading.frontend.data_utils import DataUtils as du
from PairTrading.backend.scanner import Scanner

import pandas as pd
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc  

class PairView:
    def __init__(self, pair: Pair = ["", ""], show_header=True):
        self.pair = pair
        self.show_header = show_header

        self.market_data = None
        self.callback_app = None

        #Pair Price Chart
        self.chart_pairPrice = DashChart(f"{self.pair.a}-{self.pair.b}-price-chart", "candlestick")
        self.chart_pairPrice.label = "Pair Price"
        
        #Pair Compare Chart
        self.chart_compare = DashChart(f"{self.pair.a}-{self.pair.b}-Compare-chart", "compare")
        self.chart_compare.label = "Pair Compare"

        #Pair Ratio Chart
        self.chart_ratio = DashChart(f"{self.pair.a}-{self.pair.b}-ratio-chart", "line")
        self.chart_ratio.label = "Pair Ratio"
    
    def set_pair_from_tickers(self, a, b):
        self.pair = Pair([a, b])

    def set_pair(self, pair):
        self.pair = pair

    def set_callback_app(self, app):
        self.callback_app = app

        #pair price chart
        self.chart_pairPrice.callback_inputs.append(Input('force-update', 'value'))
        self.chart_pairPrice.callback_inputs.append(Input("save-info-button", "n_clicks"))
        self.chart_pairPrice.pre_callback_functions.append(self.update_pair_price_df)
        self.chart_pairPrice.set_callback_app(self.callback_app)
        
        #pair ratio chart
        self.chart_ratio.callback_inputs.append(Input('force-update', 'value'))
        self.chart_ratio.callback_inputs.append(Input("save-info-button", "n_clicks"))
        self.chart_ratio.pre_callback_functions.append(self.update_pair_ratio_df)
        self.chart_ratio.set_callback_app(self.callback_app)

        #Compare chart
        self.chart_compare.set_callback_app(self.callback_app)

        @app.callback( Output('dummy-output', 'data', allow_duplicate=True), Input("toggle-watchlist", "value"), prevent_initial_call=True)
        def toggle_watchlist(value):
            if value:
                self.pair.watchlist = 1
            else:
                self.pair.watchlist = 0

            self.pair.save_pair_info()

        @app.callback( 
            Output("pair-price-content", "children"), 
            [
                Input("toggle-reverse", "value"),
                Input("input-ratio", "value")
            ]
        )
        def update_reverse_and_ratio(reverse, ratio):
            if not reverse and not ratio:
                return f"Pair price: ---"

            if 1 in reverse:
                self.pair.reverse = 1
            else:
                self.pair.reverse = 0

            if ratio:
                self.pair.hedge_ratio = ratio

            return f"Pair price: ${self.pair.get_price():,.2f}"
        
        @app.callback( Output('dummy-output', 'data', allow_duplicate=True), Input("input-notes", "value"), prevent_initial_call=True)
        def update_notes(value):
            if value:
                self.pair.notes = value

        @app.callback(
            Output('force-update', 'value'),
            #Output('page-content', 'children'),
            [Input('save-info-button', 'n_clicks')],
            prevent_initial_call=True
        )
        def force_update(n_clicks):
            print("Update pair info: ", self)
            self.pair.save_pair_info()
            return n_clicks

    def update_pair_price_df(self, reverse=False):
        df_a = self.market_data[self.market_data.ticker == self.pair.a]
        df_b = self.market_data[self.market_data.ticker == self.pair.b]
        
        ddf = pd.DataFrame()

        if self.pair.reverse == 1:
            ddf = df_a.merge(df_b, on='date', suffixes=['_b', '_a'])
        else:
            ddf = df_a.merge(df_b, on='date', suffixes=['_a', '_b'])

        ddf["open"] = ddf["open_a"] - ddf["open_b"] * self.pair.hedge_ratio
        ddf["close"] = ddf["close_a"] - ddf["close_b"] * self.pair.hedge_ratio
        ddf["high"] = ddf["high_a"] - ddf["high_b"] * self.pair.hedge_ratio
        ddf["low"] = ddf["low_a"] - ddf["low_b"] * self.pair.hedge_ratio

        self.chart_pairPrice._data = ddf

    def update_pair_ratio_df(self):
        df_a = self.market_data[self.market_data.ticker == self.pair.a]
        df_b = self.market_data[self.market_data.ticker == self.pair.b]

        if self.pair.reverse:
            ratio_df = (df_b.set_index("date").close / df_a.set_index("date").close).reset_index()
        else:
            ratio_df = (df_a.set_index("date").close / df_b.set_index("date").close).reset_index()

        self.chart_ratio.data = ratio_df
        return
    
    def get_layout(self):
        df_a = self.market_data[self.market_data.ticker == self.pair.a]
        df_b = self.market_data[self.market_data.ticker == self.pair.b]
        
        self.update_pair_price_df()
        self.update_pair_ratio_df()

        #Pair Compare Chart
        self.chart_compare.data = df_a
        self.chart_compare.compareData = df_b
        DVA_a = du.get_average_volume(self.pair.a) * du.get_last_price(self.pair.a)
        DVA_b = du.get_average_volume(self.pair.b) * du.get_last_price(self.pair.b)

        detail_tab = [
            #html.Div(id="pair-price-content"),
            html.P([
                html.Div(html.H4(id="pair-price-content")),
                f"{self.pair.a} Dollar Volume Average: ${DVA_a:,.0f}",html.Br(),
                f"{self.pair.b} Dollar Volume Average: ${DVA_b:,.0f}",html.Br(),
            ], style={"margin" : "2%"}),
            html.Div([
                dcc.Store(id='dummy-output'),
                html.Br(),
                dbc.Checklist(id="toggle-watchlist", options=[{"label": "Watchlist", "value": 1}],value=[self.pair.watchlist],switch=True,),
                dbc.Checklist(id="toggle-reverse", options=[{"label": "Reverse Order", "value": 1}],value=[self.pair.reverse],switch=True,),
                dbc.InputGroup([dbc.InputGroupText("Hedge Ratio"), dbc.Input("input-ratio",placeholder="Ratio", type="number", step=0.01, value=self.pair.hedge_ratio)], className="mb-3"),
                dbc.InputGroup([dbc.InputGroupText("Notes"), dbc.Textarea(id="input-notes", value=self.pair.notes)], className="mb-3"),
                dbc.Button("Save", id="save-info-button", color="primary", n_clicks=0),
                dcc.Input(id='force-update', type='hidden', value=0)
            ], style={"margin" : "2%"})
        ]

        trades_tab = dbc.Card(
            dbc.CardBody(
                    "trades"
            ),
        )
        
        #pair details card
        #header_text = f"{self.ticker_b} - {self.ticker_a}" if self.pair_info.get("reverse", 0) == 1 else f"{self.ticker_a} - {self.ticker_b}"
        header_text = f"{self.pair.a} - {self.pair.b}"
        detail_card = dbc.Card([
            dbc.CardHeader(html.H6(header_text, className="card-title")),
            dbc.CardBody(
                detail_tab
            )
        ])
        #[
            # dbc.Card([
            #     dbc.CardHeader(html.H4(f"{self.ticker_a}-{self.ticker_b} Details", className="card-title")),
                #dbc.Tabs([
                    #dbc.Tab(detail_tab, label="Details"),
                    
                    #dbc.Tab(trades_tab, label="Trades"),
                    #dbc.Tab("This tab's content is never seen", label="Tab 3", disabled=True),
                #])
            #])
        #]

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

    pair = Pair(["LNT","WEC"])
    pair_view = PairView(pair)
    #pair_view.set_pair(pair)
    pair_view.market_data = df
    pair_view.set_callback_app(app)
    
    app.layout = html.Div(
        pair_view.get_layout()
    )


    app.run_server(debug=True, port=8060, threaded=True)