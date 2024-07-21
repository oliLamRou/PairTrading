from PairTrading.frontend.charting import DashChart
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.backend.scanner import Scanner
from PairTrading.frontend.data_utils import DataUtils
from PairTrading.frontend.pair import Pair
from PairTrading.frontend.ui_pairview import PairView

from dash import Dash, html, dcc, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
import json

class ScannerView:
    def __init__(self, scanner) -> None:
        self.callback_app = None
        self.pairs_df = None
        self.max_avg_diff = 0.15
        self.scanner = scanner
        self.pairs_list = []

        #Preload pair view page
        self.pair_view = PairView("LNT", "WEC")
        self.pair_view.market_data = self.scanner.market_data(["LNT", "WEC"])
        
        #Preload chart objects
        self.compare_charts = []
        for i in range(200):
            self.comparechart = DashChart(f"tempcompare-scannerview{i}", "compare")
            self.compare_charts.append(self.comparechart)

        self.sector_dropdown = [{"label": "All", "value": 1 }]
        self.industry_list = []
        self.industry_dropdown = self.sector_dropdown

        for i, s in enumerate(self.scanner.sic_code["industry_title"].to_list()):
            #count = self.pairs_df.industry_title.value_counts().get(s, 0)
            count = 0
            self.industry_list.append(s)
            self.industry_dropdown.append({"label": f"({count}) {s}", "value": i+2})

    def set_callback_app(self, app):
        self.callback_app = app
        self.pair_view.set_callback_app(app)
        self.pairview_layout = self.pair_view.get_layout()
        for c in self.compare_charts:
            c.set_callback_app(app)

        @app.callback(
            Output("page-content", "children"),
            [
                #Input("pagination", "active_page"),
                Input("minprice", "value"),
                Input("maxprice", "value"),
                Input("industry-select", "value"),
                Input("max-avgdiff", "value"),
            ],
        )
        def apply_filter_callback(minprice, maxprice, industry, max_avg_diff):
            if minprice and maxprice and industry:
                self.max_avg_diff = max_avg_diff
                return self.filter_pairs(self.industry_list[int(industry)-2])
            
        @app.callback(
            Output("modal-details", "is_open"),
            Output("pairview-header-content", "children"),
            Output("pairview-content", "children"),
            Input({"type": "open-details", "index": ALL}, "n_clicks"),
            State("modal-details", "is_open"),
        )
        def toggle_details(n, is_open):
            print("toggle")
            for p in ctx.triggered:
                invoker = p["prop_id"]
                invoker_index = json.loads(invoker.split('.')[0])["index"]  
                ticker_a = self.pairs_list[invoker_index][0]
                ticker_b = self.pairs_list[invoker_index][1]              
                #print(invoker_index, self.pairs_list[invoker_index])
                
                if n[invoker_index]:
                    self.pair_view.ticker_a = ticker_a
                    self.pair_view.ticker_b = ticker_b
                    self.pair_view.market_data = self.scanner.market_data([ticker_a, ticker_b])
                    return not is_open, html.H6(f"{ticker_a}, {ticker_b} - Pair View"), self.pair_view.get_layout()
     
            return is_open, "nothing", "nothing"

    
    def get_layout(self):
        scanner_settings = html.Div([
            dbc.Card([       
                dbc.CardHeader(html.H6("Scanner Filter", className="card-title")),
                dbc.CardBody([
                    dbc.InputGroup([dbc.InputGroupText("Min Price"), dbc.Input(id="minprice", type="number", value=2)]),
                    dbc.InputGroup([dbc.InputGroupText("Max Price"), dbc.Input(id="maxprice", type="number", value=10)]),
                    dbc.InputGroup([dbc.InputGroupText("Sector"), dbc.Select(id="industry-select", options = self.sector_dropdown, value="All")]),
                    dbc.InputGroup([dbc.InputGroupText("Max Average Difference"), dbc.Input(id="max-avgdiff", type="number", value=self.max_avg_diff)])
                ])
            ])
        ])

        details_modal = dbc.Modal(
            [
                dbc.ModalHeader(html.Div(id="pairview-header-content")),
                dbc.ModalBody( html.Div(id="pairview-content")),
            ],
            id="modal-details",
            fullscreen=True,
            is_open=False,
        )

        return [scanner_settings, html.Div(id="result-content"), html.Div(id="page-content"), details_modal]

    def filter_pairs(self, industry):
        self.pairs_list = []
        layout_elements = []
        chart_counter = 0
        
        self.scanner.industry = industry
        pairs_df = self.scanner.get_pairs
        
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

            chart_card = chart.get_layout()
            detail_card = dbc.Card([
                dbc.CardBody("Details"),
            ])

            pair_card = dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col(chart_card, width=6),
                        dbc.Col(detail_card, width=3),
                        dbc.Col(dbc.Button("Details", id={"type" : "open-details", "index" : i}), width=3),
                    ])
                ]),
            ])

            layout_elements.append(pair_card)
            i += 1

        return layout_elements


if __name__ == '__main__':
    print("ui_scannerview")
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

    scanner=Scanner()
    scanner.min_price = 2
    scanner.max_price = 200
    scanner.min_vol = 100000
    
    scanner_view = ScannerView(scanner)
    scanner_view.set_callback_app(app)

    app.layout = html.Div(
        scanner_view.get_layout()
    )

    app.run_server(debug=True)