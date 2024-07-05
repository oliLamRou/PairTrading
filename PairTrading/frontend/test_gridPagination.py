from PairTrading.frontend.charting import DashChart
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.frontend.data_utils import DataUtils
from PairTrading.frontend.pair import Pair

from PairTrading.src import _constant
import pandas as pd

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

dw = DataWrangler()
df = dw.market_data("AA")
print(df)

chart1 = DashChart("AA", "candlestick")
chart1.data = df
chart1.set_callback_app(app)

df = dw.market_data("AU")
chart2 = DashChart("AU", "line")
chart2.data = df
chart2.set_callback_app(app)

def out_page1():
    ChartCard = [
        dbc.CardBody([
            dbc.Row([
                #dbc.Col("papate"),
                dbc.Col(chart1.get_layout()),
                
            ])
        ])                
    ]

    chartCard = dbc.Card(
        ChartCard
    )  
    
    return chartCard


def out_page2():
    ChartCard = [
        dbc.CardBody([
            dbc.Row([
                dbc.Col(chart2.get_layout()),
            ])
        ])                
    ]

    chartCard = dbc.Card(
        ChartCard
    )  
    
    return chartCard, out_page1()

app.layout = html.Div([
    #dcc.Input(id='pagination', value=1, type="number", step=1),
    dbc.Pagination(id="pagination", max_value=100, first_last=False, fully_expanded=False, previous_next=False),
    html.Div(id="page-content"),
])

@app.callback(
    Output("page-content", "children"),
    [Input("pagination", "active_page")]
)
def change_page(value):
    if value:
        print(value)
        if value == 1:
            return out_page1()
        if value == 2:
            return out_page2()
    
    return "Select a page"

app.run_server(debug=True, port=8060)