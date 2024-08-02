import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, ctx, ALL
from PairTrading.backend.scanner import Scanner

tickers = ['AAPL', 'MSTR', 'NVDA']
tickers2 = ['ARKG', 'ARKK']

def get_charts(t):
    charts = []
    for i, ticker in enumerate(t):
        new = dbc.Row([
            dbc.Col(dbc.Button(ticker, id={'type': 'details_button', 'index': i}))
        ])
        charts.append(new)
    return charts

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

@app.callback(
    Output("details_id", "children"),
    [Input({'type': 'details_button', 'index': ALL}, 'n_clicks')],
    [Input('ticker_store', 'data')]
)
def show_details(n_clicks, stored_tickers):
    if not ctx.triggered or not n_clicks:
        return "No button clicked yet"
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    button_index = eval(button_id)['index']
    ticker = stored_tickers[button_index]
    return dcc.Markdown(f"Details for {ticker}")

@app.callback(
    [
        Output("page-content", "children"), 
        Output('ticker_store', 'data')
    ],
    [Input("button_id", 'n_clicks')],
    prevent_initial_call=True
)
def show_charts(n_clicks):
    if n_clicks is None:
        n_clicks = 0
    return get_charts(tickers2), tickers2

if __name__ == '__main__':
    app.layout = html.Div([
        dcc.Store(id='ticker_store', data=tickers),
        dbc.Card(id='details_id'),
        dbc.Button("Load Details", id='button_id'),
        dbc.Card(get_charts(tickers), id='page-content')
    ])

    app.run_server(debug=True)
    app.stop()
