from PairTrading.frontend.charting import DashChart
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.backend.scanner import Scanner
from PairTrading.frontend.data_utils import DataUtils
from PairTrading.frontend.pair import Pair
import pandas as pd

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions=True
app.title="Scanner Vue"

d = DataUtils()
dw = DataWrangler()
df = dw._DataWrangler__polygon_db.get_table('market_data')

#Scanner settings
sic_df = dw.sic_code()
sic_df = sic_df[sic_df.office == 'Office of Energy & Transportation']
sector_list = dw.sic_code()['office'].sort_values().unique()

sector_dropdown = [{"label": "All", "value": 1 }]
industry_dropdown = sector_dropdown

for i, s in enumerate(sector_list):
    sector_dropdown.append({"label": s, "value": i+2})

scanner_settings = html.Div([
    dbc.Card([       
        dbc.CardHeader(html.H6("Scanner Filter", className="card-title")),
        dbc.CardBody([
            dbc.InputGroup([dbc.InputGroupText("Min Price"), dbc.Input(id="minprice", type="number", placeholder=2)]),
            dbc.InputGroup([dbc.InputGroupText("Max Price"), dbc.Input(id="maxprice", type="number", placeholder=10)]),
            #dbc.InputGroup([dbc.InputGroupText("Min Volume"), dbc.Input(placeholder="Min Volume")]),
            #dbc.InputGroup([dbc.InputGroupText("Max Volume"), dbc.Input(placeholder="Max Volume")]),
            dbc.InputGroup([dbc.InputGroupText("Sector"), dbc.Select(id="sector-select", options = sector_dropdown, placeholder="All")])
        ])
    ])
])

#Charts page content
charts = []
for i in range(200):
    chart = DashChart(f"temp{i}", "line")
    chart.set_callback_app(app)
    charts.append(chart)

def get_chart_page(minprice, maxprice, sector):
    chart_counter = 0
    layout_elements = []

    scanner = Scanner()
    scanner.min_price = minprice
    scanner.max_price = maxprice
    scanner.min_vol = 0
    scanner.office = sector
    tickers = scanner.filtered_tickers()

    i = 0

    max_tickers = 15

    for t in tickers:
        df_ = df[df.ticker == t]
        if df_.empty or t.find(".") >= 0:
            continue

        i += 1
        if i > max_tickers:
            break
    
        chart_compare = charts[chart_counter]
        chart_compare.label = t
        chart_counter += 1
        chart_compare.data = df_

        ChartCard = [
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(chart_compare.get_layout(),width=6),
                ])
            ])                
        ]

        chartCard = dbc.Card(
            ChartCard
        )  
        
        layout_elements.append(chartCard)

    return layout_elements

app.layout = html.Div([
    #dcc.Input(id='pagination', value=1, type="number", step=1),
    scanner_settings,
    html.Div(id="result-content"),
    #dbc.Pagination(id="pagination", max_value=100, first_last=False, fully_expanded=False, previous_next=False),
    html.Div(id="page-content")
])

@app.callback(
    Output("page-content", "children"),
    [
        #Input("pagination", "active_page"),
        Input("minprice", "value"),
        Input("maxprice", "value"),
        Input("sector-select", "value")
    ],
)

def change_page(minprice, maxprice, sector):
    if minprice and maxprice and sector:
        print(sector_dropdown[int(sector)-1]["label"])
        return get_chart_page(minprice, maxprice, sector_dropdown[int(sector)-1]["label"])

    #return sector_dropdown[int(sector)-1]["label"]

app.run_server(debug=True, port=8060)