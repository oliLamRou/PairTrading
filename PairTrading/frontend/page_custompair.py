
from PairTrading.frontend.pair import Pair
from PairTrading.backend.scanner import Scanner
from PairTrading.frontend.ui_pairview import PairView
from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc 

print("page_custompair")
scanner=Scanner()
scanner.min_price = 2
scanner.max_price = 200
scanner.min_vol = 100000

app = Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN])

pair = Pair(["LNT","WEC"])
pair_view = PairView(pair, show_header=True)
pair_view.set_callback_app(app)

@app.callback(
    Output("page-content", "children"), 
    State("input-pair", "value"),
    Input("load-pair-button", "n_clicks"),
)
def load_pair(value, n_clicks): 
    if value == None:
        return 
    print(value)
    p = sorted(str.upper(value).replace(" ", "").split(","), key=str.casefold)
    print(p)
    pair_view.set_pair_from_tickers(p[0], p[1])
    pair_view.market_data = scanner.market_data(p)
    return pair_view.get_layout()

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.InputGroup([dbc.InputGroupText("Pair"), dbc.Input("input-pair",placeholder="A, B")], className="mb-3"),
        ]),
        dbc.Col([
            dbc.Button("Load", id="load-pair-button", color="primary", n_clicks=0)
        ])
    ]),
    dbc.Row(
        dbc.Col(
            html.Div(id="page-content")
        )
    )

])

app.run_server(debug=True, port=8060, threaded=True)


