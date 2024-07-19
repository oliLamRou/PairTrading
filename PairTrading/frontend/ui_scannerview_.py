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
        print("set callback app")
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

        return [scanner_settings, html.Div(id="page-content")]

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

scanner=Scanner()
scanner.min_price = 5
scanner.max_price = 200
scanner.min_vol = 100000
scanner.industry = 'SERVICES-AUTOMOTIVE REPAIR, SERVICES & PARKING'


def get_charts(n_clicks):
    charts = []
    print(n_clicks)
    for A in tickers:
        new = dbc.Row([
            dbc.Col(dcc.Markdown(A, id=A)),
            dbc.Col(dbc.Button(A, id={"type": "AAA", "index": 'n_clicks'})),
        ])
        charts.append(new)

    return charts

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
@app.callback(
    Output("details_id", "children"),
    Input({'type': 'AAA', 'index': ALL}, 'values'),
)
def charts(n_clicks):
    return dcc.Markdown(n_clicks)

@app.callback(
    Output("page-content", "children"),
    [
        Input("button_id", 'n_clicks'),
    ]
)
def show(n_clicks):
    df = tickers
    # if df.empty:
    #     return dcc.Markdown('Empty')

    return get_charts(n_clicks)

tickers = ['AAPL', 'MSTR', 'NVDA']

if __name__ == '__main__':    
    # print([Input(A, 'n_clicks') for A in scanner.get_pairs.A])
    app.layout = html.Div([
        dbc.Card(id='details_id'),
        dbc.Button("Details", id='button_id'),
        dbc.Card(id='page-content')
    ])

    app.run_server(debug=True)