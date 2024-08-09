import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, ctx, ALL
from PairTrading.backend.scanner import Scanner

s = Scanner()

def get_charts(pairs):
    charts = []
    for i, row in pairs.iterrows():
        new = dbc.Row([
            dbc.Col(dbc.Button(row.A + ' ' + row.B, id={'type': 'details_button', 'index': i}))
        ])
        charts.append(new)
    return charts

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

@app.callback(
    Output("details_id", "children"),
    [Input({'type': 'details_button', 'index': ALL}, 'n_clicks')],
    [Input('ticker_store', 'data')],
    prevent_initial_call=True
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
    [Input("industry_dropdown", 'value')],
    prevent_initial_call=True
)
def show_charts(value):
    if not value:
        return []

    s.industry = value
    pairs = s.get_pairs
    pairs['pairs'] = pairs.A + '__' + pairs.B
    return get_charts(pairs), pairs['pairs'].to_list()

if __name__ == '__main__':
    pp = s.potential_pair
    x = pp[pp.potential_pair > 100]
    dropdown_values = [{"label": industry, "value": industry} for industry in x.industry.to_list()]
    app.layout = html.Div([
        dcc.Store(id='ticker_store'),
        dbc.Card(id='details_id'),
        # dbc.Button("Load Details", id='button_id'),
        dbc.Select(dropdown_values, id='industry_dropdown'),
        dbc.Card(id='page-content')
    ])

    app.run_server(debug=True)
