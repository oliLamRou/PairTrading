import copy
from PairTrading.frontend.charting import DashChart
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.frontend.data_utils import DataUtils
from PairTrading.frontend.pair import Pair

from PairTrading.src import _constant
import pandas as pd

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions=True
app.title="ScannerVue"

d = DataUtils()
charts = []

for i in range(200):
    chart = DashChart(f"temp{i}", "line")
    chart.set_callback_app(app)
    charts.append(chart)

dw = DataWrangler()
df = dw._DataWrangler__polygon_db.get_table('market_data')
tickers = dw.market_snapshot().ticker

def get_chart_page(value):
    chart_counter = 0
    layout_elements = []
    i = 0
    max_tickers = 25

    for t in tickers:
        df_ = df[df.ticker == t]
        if df_.empty or t.find(".") >= 0:
            continue

        i += 1
        if i > max_tickers:
            break
    
        chart_compare = charts[chart_counter]
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
    dbc.Pagination(id="pagination", max_value=100, first_last=False, fully_expanded=False, previous_next=False),
    html.Div(id="page-content")
])

@app.callback(
    Output("page-content", "children"),
    [Input("pagination", "active_page")],
)

def change_page(value):
    if value:
        print(value)
        if value == 2:
            return get_chart_page(value)
        if value == 1:
            return "patatie patata"

    return "Select a page"

app.run_server(debug=True, port=8060)