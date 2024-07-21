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
    def __init__(self, ticker_a, ticker_b, diff_average=1, ratio=1, show_header=True):
        self.ticker_a = ticker_a
        self.ticker_b = ticker_b
        self.show_header = show_header

        self.pair_info = self.get_pair_info().to_dict()
        self.updated_pair_info = {}

        #self.diff_average = diff_average
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

        #pair price chart
        #self.chart_pairPrice.callback_inputs.append(Input("toggle-reverse", "value"))
        #self.chart_pairPrice.callback_inputs.append(Input("input-ratio", "value"))
        self.chart_pairPrice.callback_inputs.append(Input('force-update', 'value'))
        self.chart_pairPrice.callback_inputs.append(Input("save-info-button", "n_clicks"))
        self.chart_pairPrice.pre_callback_functions.append(self.precall)
        self.chart_pairPrice.pre_callback_functions.append(self.update_pair_price_df)
        self.chart_pairPrice.post_callback_functions.append(self.postcall)
        self.chart_pairPrice.set_callback_app(self.callback_app)

        self.chart_compare.set_callback_app(self.callback_app)
        self.chart_ratio.set_callback_app(self.callback_app)

        @app.callback( Output('dummy-output', 'data', allow_duplicate=True), Input("toggle-watchlist", "value"), prevent_initial_call=True)
        def toggle_watchlist(value):
            if value:
                self.update_pair_info({"watchlist" : 1})
            else:
                self.update_pair_info({"watchlist" : 0})

        @app.callback( 
            Output("pair-price-content", "children"), 
            [
                Input("toggle-reverse", "value"),
                Input("input-ratio", "value")
            ]
        )
        def toggle_reverse(reverse, ratio):
            print("update pair price content")
            print(reverse, ratio)

            if not reverse and not ratio:
                return f"Pair price: ---"

            if 1 in reverse:

                self.updated_pair_info["pair_order"] = 1
                print("reverse")
                
            else:
                #update_dict["pair_order"] = 0
                self.updated_pair_info["pair_order"] = 0
                #self.reverse = 0
                print("Not reversed")

            if ratio:
                self.updated_pair_info["hedge_ratio"] = ratio
                #update_dict["hedge_ratio"] = ratio
                #self.ratio = ratio

            #self.update_pair_info(update_dict)
            return f"Pair price: {self.get_pair_price()}"
        
        @app.callback( Output('dummy-output', 'data', allow_duplicate=True), Input("input-notes", "value"), prevent_initial_call=True)
        def update_notes(value):
            if value:
                self.update_pair_info({"notes" : value})

        # @app.callback( 
        #     Output('save-info-button', "value"),
        #     Input("save-info-button", "n_clicks"), 
        #     prevent_initial_call=True
        # )
        # def save_button(n_clicks):
        #     print("sssssssssave", n_clicks)
        #     self.update_pair_info(self.pair_info)

        @app.callback(
            Output('force-update', 'value'),
            [Input('save-info-button', 'n_clicks')]
        )
        def force_update(n_clicks):
            print("Update pair info: ", self.updated_pair_info)
            self.update_pair_info(self.updated_pair_info)
            return n_clicks

    def save_pair_info(self):
        self.update_pair_info(self.pair_info)

    def get_pair_price(self):
        ratio = self.updated_pair_info.get("hedge_ratio", self.updated_pair_info.get("hedge_ratio"))
        if self.updated_pair_info["pair_order"]:
            pair_price = du.get_last_price(self.ticker_b) - (du.get_last_price(self.ticker_a) * ratio)
        else:
            pair_price = du.get_last_price(self.ticker_a) - (du.get_last_price(self.ticker_b) * ratio)
        return pair_price

    def update_pair_price_df(self, reverse=False):
        print("update DF")
        df_a = self.market_data[self.market_data.ticker == self.ticker_a]
        df_b = self.market_data[self.market_data.ticker == self.ticker_b]
        
        ddf = pd.DataFrame()

        #ddf = self.chart_pairPrice._data
        rev = self.get_pair_info().get("pair_order", 0)
        ratio = self.get_pair_info().get("hedge_ratio", 0)
        print("REVERSE: ", rev)

        if rev == 1:
            ddf = df_a.merge(df_b, on='date', suffixes=['_b', '_a'])
        else:
            ddf = df_a.merge(df_b, on='date', suffixes=['_a', '_b'])

        ddf["open"] = ddf["open_a"] - ddf["open_b"] * ratio
        ddf["close"] = ddf["close_a"] - ddf["close_b"] * ratio
        ddf["high"] = ddf["high_a"] - ddf["high_b"] * ratio
        ddf["low"] = ddf["low_a"] - ddf["low_b"] * ratio

        #print(ddf)
        self.chart_pairPrice._data = ddf

        print("finished update DF")

    def precall(self): 
        print()
        print("Pre-callback")

    def postcall(self): 
        print("Post-callback")

    def update_pair_info(self, info: dict):
        dw = DataWrangler()
        return dw.update_pair_info([self.ticker_a, self.ticker_b], info)
        
    def get_pair_info(self):
        dw = DataWrangler()
        return dw.get_pair_info([self.ticker_a, self.ticker_b])
    
    def get_layout(self):
        
        df_a = self.market_data[self.market_data.ticker == self.ticker_a]
        df_b = self.market_data[self.market_data.ticker == self.ticker_b]
        
        #Pair Price Chart
        print("Get Layout")
        #self.update_pair_price_df(self.pair_info.get("pair_order", 0)) pair_info.get("ratio")
        self.update_pair_price_df()

        #Pair Compare Chart
        self.chart_compare.data = df_a
        self.chart_compare.compareData = df_b

        #Pair Ratio Chart
        ratio_df = (df_a.set_index("date").close / df_b.set_index("date").close).reset_index()
        self.chart_ratio.data = ratio_df
            
        detail_tab = [
            #html.Div(id="pair-price-content"),
            html.P([
                html.Div(html.H6(id="pair-price-content")),
                "Average Difference: xxxx",html.Br(),
                f"{self.ticker_a} Dollar Volume Average: ",html.Br(),
                f"{self.ticker_b} Dollar Volume Average: ",html.Br(),
            ], style={"margin" : "2%"}),
            html.Div([
                dcc.Store(id='dummy-output'),
                html.Br(),
                dbc.Checklist(id="toggle-watchlist", options=[{"label": "Watchlist", "value": 1}],value=[self.get_pair_info().get('watchlist', 0)],switch=True,),
                dbc.Checklist(id="toggle-reverse", options=[{"label": "Reverse Order", "value": 1}],value=[self.get_pair_info().get('pair_order', [])],switch=True,),
                dbc.InputGroup([dbc.InputGroupText("Hedge Ratio"), dbc.Input(id="input-ratio",placeholder="Ratio", type="number", step=0.01, value=self.pair_info.get("hedge_ratio"))], className="mb-3"),
                dbc.InputGroup([dbc.InputGroupText("Notes"), dbc.Textarea(id="input-notes", value=self.get_pair_info().get('notes', []))], className="mb-3"),
                
                #dbc.Button("Reset", color="primary", disabled=True),
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
        detail_card = dbc.Card(
            dbc.CardBody(
                detail_tab
            )
        )
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


    app.run_server(debug=True, port=8060, threaded=True)