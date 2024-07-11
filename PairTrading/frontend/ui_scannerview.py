from PairTrading.frontend.charting import DashChart
from PairTrading.backend.scanner import Scanner
from PairTrading.frontend.data_utils import DataUtils as du
from PairTrading.frontend.ui_pairview import PairView
from PairTrading.backend.data_wrangler import DataWrangler

from dash import Dash, html, dcc, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
import json

class ScannerView:
    def __init__(self, scanner) -> None:
        self.dw = DataWrangler()
        self.callback_app = None
        self.pairs_df = None
        self.max_avg_diff = 0.15
        self.scanner = scanner
        self.pairs_list = []

        self.pair_view = PairView()
        self.update_industry_dropdown()
        
        #Preload chart objects
        self.compare_charts = []
        for i in range(200):
            self.comparechart = DashChart(f"tempcompare-scannerview{i}", "compare")
            self.compare_charts.append(self.comparechart)

    def set_callback_app(self, app):
        self.callback_app = app
        self.pair_view.set_callback_app(app)
        for c in self.compare_charts:
            c.set_callback_app(app)

        @app.callback(
            Output("page-content", "children"),
            #Input({"type": "refresh-page-content", "index": ALL}, "value"),
            [
                #Input("pagination", "active_page"),
                Input("minprice", "value"),
                Input("maxprice", "value"),
                Input("min_avg_vol", "value"),
                Input("industry-select", "value"),
                Input("max-avgdiff", "value"),
            ],
        )
        def apply_filter_callback(minprice, maxprice, min_avg_vol, industry, max_avg_diff):
            if industry == "1":
                return ""
              
            if minprice and maxprice and industry and min_avg_vol:
                self.max_avg_diff = max_avg_diff

                return self.filter_pairs(self.industry_list[int(industry)-2])
            
            return ""

        # @app.callback(
        #     Output("loader-content", "children"),
        #     Input("loader-output", "data"),
        # )
        # def apply_filter_callback(*args):
        #     print(args)
        #     return "loading"
            
        @app.callback(
            Output("modal-details", "is_open"),
            Output("pairview-header-content", "children"),
            Output("pairview-content", "children"),
            Input({"type": "open-details", "index": ALL}, "n_clicks"),
            State("modal-details", "is_open"),
        )
        def toggle_details(n, is_open):
            for p in ctx.triggered:
                invoker = p["prop_id"]

                if invoker == ".":
                    continue

                invoker_index = json.loads(invoker.split('.')[0])["index"]  
                ticker_a = self.pairs_list[invoker_index][0]
                ticker_b = self.pairs_list[invoker_index][1]              
                
                if n[invoker_index]:
                    self.pair_view.set_tickers(ticker_a, ticker_b)
                    self.pair_view.market_data = self.scanner.market_data([ticker_a, ticker_b])
                    self.pairview_layout = self.pair_view.get_layout()
                    return not is_open, html.H6(f"{ticker_a}, {ticker_b} - Pair View"), self.pair_view.get_layout()
     
            return is_open, "nothing", "nothing"

    def update_industry_dropdown(self):
        ppairs = self.scanner.potential_pair.sort_values("potential_pair", ascending=False)
        industry_list = ppairs["industry"].to_list()

        self.sector_dropdown = [{"label": "---", "value": 1 }]
        self.industry_list = []
        self.industry_dropdown = self.sector_dropdown

        for i, industry in enumerate(industry_list):
            industry_df = ppairs[ppairs["industry"] == industry]
            if industry_df.empty:
                count = 0
            else:
                count = industry_df.get("potential_pair").iloc[0]
                self.industry_list.append(industry)
                self.industry_dropdown.append({"label": f"({count}) {industry}", "value": i+2})
    
    def get_pairs_callback(self, percent):
        return

    def filter_pairs(self, industry):
        self.pairs_list = []
        layout_elements = []
        chart_counter = 0
        
        self.scanner.industry = industry
        pairs_df = self.scanner.get_pairs(self.get_pairs_callback)
        
        if pairs_df.empty:
            return None
        
        filtered_pairs_df = pairs_df[(pairs_df.avg_diff <= self.max_avg_diff)].reset_index(drop=True).sort_values(by=("avg_diff"), ascending=True).reset_index()

        i = 0
        max_tickers = 50
        for i, row in filtered_pairs_df.iterrows():
            ticker_a = row.A
            ticker_b = row.B
            avg_diff = row.avg_diff

            tickera_df = self.scanner.market_data([ticker_a])
            tickerb_df = self.scanner.market_data([ticker_b])
            self.pairs_list.append([ticker_a, ticker_b])

            if i > max_tickers:
                break
        
            chart = self.compare_charts[chart_counter]
            chart.chartType = "compare"
            chart.label = f"{i}. {ticker_a} - {ticker_b} - {avg_diff}"
            chart.data = tickera_df
            chart.compareData = tickerb_df
            chart_counter += 1

            info_a = self.dw.ticker_info(ticker_a)
            info_b = self.dw.ticker_info(ticker_b)

            #Check default watchlist value
            pair_info = self.dw.get_pair_info([ticker_a, ticker_b]).fillna(0).to_dict()

            chart_card = chart.get_layout()
            detail_card = dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6(ticker_a),
                            info_a['name'].values[0], html.Br(),html.Br(),
                            f"Last Price: ${du.get_last_price(ticker_a):,.2f}",html.Br(),
                            f"Market Cap: {du.format_large_number(info_a.get('market_cap').values[0])}",html.Br(),
                            f"Shares Outstanding: {du.format_large_number(info_a.get('share_class_shares_outstanding').values[0])}",html.Br(),
                            f"Volume: {du.format_large_number(du.get_average(ticker_a, 'volume', period=1))}", html.Br(),
                            f"Average Volume (30D): {du.format_large_number(du.get_average_volume(ticker_a))}",
                        ]),
                        dbc.Col([
                            html.H6(ticker_b),
                            info_b['name'].values[0], html.Br(),html.Br(),
                            f"Last Price: ${du.get_last_price(ticker_b):,.2f}",html.Br(),
                            f"Market Cap: {du.format_large_number(info_b.get('market_cap').values[0])}",html.Br(),
                            f"Shares Outstanding: {du.format_large_number(info_b.get('share_class_shares_outstanding').values[0])}",html.Br(),
                            f"Volume: {du.format_large_number(du.get_average(ticker_b, 'volume', period=1))}", html.Br(),
                            f"Average Volume (30D): {du.format_large_number(du.get_average_volume(ticker_b))}",
                        ]),
                    ])
                ]),
                dbc.Row([
                    dbc.Col(dbc.Button("Details", id={"type" : "open-details", "index" : i}), width=2),
                    dbc.Col(dbc.Checklist(id={"type" : "scannerview-toggle-watchlist", "index" : i}, options=[{"label": "Watchlist", "value": 1, "disabled" : True}],value=[pair_info.get('watchlist', 0)])),
                ],style={"margin" : "2%"}),
            ])

            pair_card = dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(chart_card, width=6),
                        dbc.Col(detail_card, width=4)
                        #dbc.Col(dbc.Button("Details", id={"type" : "open-details", "index" : i}), width=2),
                    ]),
                ]),
            ])

            layout_elements.append(pair_card)
            i += 1

        return layout_elements

    def get_layout(self):
        scanner_settings = html.Div([
            dcc.Store(id='loader-output'),
            dbc.Card([       
                dbc.CardHeader(html.H6("Scanner Filter", className="card-title")),
                dbc.CardBody([
                    dbc.InputGroup([dbc.InputGroupText("Min Price"), dbc.Input(id="minprice", type="number", value=10)]),
                    dbc.InputGroup([dbc.InputGroupText("Max Price"), dbc.Input(id="maxprice", type="number", value=200)]),
                    dbc.InputGroup([dbc.InputGroupText("Min 30D Average Volume"), dbc.Input(id="min_avg_vol", type="number", value=50000)]),
                    dbc.InputGroup([dbc.InputGroupText("Industry"), dbc.Select(id="industry-select", options = self.industry_dropdown, value="---")]),
                    #dbc.InputGroup([dbc.InputGroupText("Sector"), dbc.Select(id={"type" : "refresh-page-content", "index" : 1}, options = self.sector_dropdown, value="All")]),
                    dbc.InputGroup([dbc.InputGroupText("Max Average Difference"), dbc.Input(id="max-avgdiff", type="number", value=self.max_avg_diff)])
                ])
            ])
        ])

        details_modal = dbc.Modal([
            dbc.ModalHeader(html.Div(id="pairview-header-content")),
            dbc.ModalBody( html.Div(id="pairview-content")),
        ],
            id="modal-details",
            fullscreen=True,
            is_open=False,
        )

        return [scanner_settings, html.Div(id="loader-content"), html.Div(id="page-content"), details_modal]
    
if __name__ == '__main__':
    print("ui_scannerview")
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

    scanner=Scanner()
    scanner.min_price = 2
    scanner.max_price = 200
    scanner.min_avg_vol = 10000
    
    scanner_view = ScannerView(scanner)
    scanner_view.set_callback_app(app)

    app.layout = html.Div(
        scanner_view.get_layout()
    )

    app.run_server(debug=True)