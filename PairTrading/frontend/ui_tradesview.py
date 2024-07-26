from PairTrading.frontend.charting import DashChart
import time
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.frontend.pair import Pair
from PairTrading.frontend.data_utils import DataUtils as du
from PairTrading.backend.scanner import Scanner

import pandas as pd
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc  

class TradeView:
    def __init__(self, pair: Pair = ["", ""], show_header=True):
        self.pair = pair

        #Pair Ratio Chart
        self.chart_price = DashChart(f"{self.pair.a}-{self.pair.b}-trade-chart", "line")
        self.chart_price.label = "Trades History"

        ##### trade data {fill_a, fill_b, complete_time_a, complete_time_b, amount_a, amount_b}

    def set_callback_app(self, app):
        self.callback_app = app

        #pair price chart
        #self.chart_price.callback_inputs.append(Input('force-update', 'value'))
        #self.chart_price.callback_inputs.append(Input("save-info-button", "n_clicks"))
        #self.chart_price.pre_callback_functions.append(self.update_pair_price_df)
        self.chart_price.set_callback_app(self.callback_app)

        
        # @app.callback(
        #     Output('force-update', 'value'),
        #     #Output('page-content', 'children'),
        #     [Input('save-info-button', 'n_clicks')],
        #     prevent_initial_call=True
        # )
        # def force_update(n_clicks):
        #     print("Update pair info: ", self)
        #     self.pair.save_pair_info()
        #     return n_clicks

        
    def get_layout(self):

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

        self.chart_price._data = ddf
        
        header_text = f"{self.pair.a} - {self.pair.b}"
        detail_card = dbc.Card([
            dbc.CardHeader(html.H6(header_text, className="card-title")),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            f"{self.pair.a}",html.Br(),
                            dbc.InputGroup([
                                dbc.InputGroupText("Amount"), dbc.Input(placeholder="", type="number", step=1)
                            ]),
                            dbc.InputGroup([
                                dbc.InputGroupText("Completed Time"), dbc.Input(placeholder="", type="text")
                            ]),
                            dbc.InputGroup([
                                dbc.InputGroupText("Fill Price"), dbc.Input(placeholder="", type="number", step=0.01)
                            ])
                        ])
                    ),
                    dbc.Col(
                        html.Div([
                            f"{self.pair.b}",html.Br(),
                            dbc.InputGroup([
                                dbc.InputGroupText("Amount"), dbc.Input(placeholder="", type="number", step=1)
                            ]),
                            dbc.InputGroup([
                                dbc.InputGroupText("Completed Time"), dbc.Input(placeholder="", type="text")
                            ]),
                            dbc.InputGroup([
                                dbc.InputGroupText("Fill Price"), dbc.Input(placeholder="", type="number", step=0.01)
                            ])
                        ])
                    )
                ]),
                dbc.Row(
                    dbc.Col(dbc.Button("Add Trade", id="add-trade-button", color="primary", n_clicks=0))
                )
            ])
        ])

        #pair view card
        trades_card = [
            dbc.Row([
                #charts
                dbc.Col([
                    dbc.Row(dbc.Col(self.chart_price.get_layout())),
                ], width="8"),

                #details
                dbc.Col(
                    dbc.Row(dbc.Col(detail_card))
                )
            ])

        ]
       
        layout_elements = [
            html.Div(trades_card)
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
    trade_view = TradeView(pair)
    trade_view.market_data = df
    trade_view.set_callback_app(app)
    
    app.layout = html.Div(
        trade_view.get_layout()
    )


    app.run_server(debug=True, port=8060, threaded=True)