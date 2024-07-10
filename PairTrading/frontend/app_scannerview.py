from PairTrading.frontend.charting import DashChart
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.backend.scanner import Scanner
from PairTrading.frontend.data_utils import DataUtils
from PairTrading.frontend.pair import Pair
import pandas as pd
import numpy as np
import plotly.express as px

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions=True
app.title="Scanner Vue"

d = DataUtils()
dw = DataWrangler()
df = dw._DataWrangler__polygon_db.get_table('market_data')

#Scanner settings
scanner = Scanner()

#sic_df = dw.sic_code()
#sic_df = sic_df[sic_df.office == 'Office of Energy & Transportation']
#sector_list = dw.sic_code()['office'].sort_values().unique()
#industry_list = 

scanner.min_price = 2
scanner.max_price = 50
scanner.min_vol = 1000000
#scanner.office = None
pairs_df = scanner.get_pairs()

sector_dropdown = [{"label": "All", "value": 1 }]
industry_dropdown = sector_dropdown
#industry_dropdown = pairs_df.industry_title.sort_values().unique()

results = 0

for i, s in enumerate(pairs_df.industry_title.sort_values().unique()):
    industry_dropdown.append({"label": s, "value": i+2})

scanner_settings = html.Div([
    dbc.Card([       
        dbc.CardHeader(html.H6("Scanner Filter", className="card-title")),
        dbc.CardBody([
            dbc.InputGroup([dbc.InputGroupText("Min Price"), dbc.Input(id="minprice", type="number", value=2)]),
            dbc.InputGroup([dbc.InputGroupText("Max Price"), dbc.Input(id="maxprice", type="number", value=10)]),
            #dbc.InputGroup([dbc.InputGroupText("Min Volume"), dbc.Input(placeholder="Min Volume")]),
            #dbc.InputGroup([dbc.InputGroupText("Max Volume"), dbc.Input(placeholder="Max Volume")]),
            dbc.InputGroup([dbc.InputGroupText("Sector"), dbc.Select(id="industry-select", options = sector_dropdown, value="All")]),
            dbc.Checkbox(id="scan-pairs", label="Scan Pairs", value=True)
        ])
    ])
])

#Charts page content
line_charts = []
compare_charts = []
for i in range(200):
    linechart = DashChart(f"templine{i}", "line")
    linechart.set_callback_app(app)
    line_charts.append(linechart)

    comparechart = DashChart(f"tempcompare{i}", "compare")
    comparechart.set_callback_app(app)
    compare_charts.append(comparechart)

### si je cree le scanner ici au lieu de ligne 59
#scanner = Scanner()

def show_filtered_tickers(minprice, maxprice, industry):
    chart_counter = 0
    layout_elements = []

    scanner = Scanner()
    scanner.min_price = minprice
    scanner.max_price = maxprice
    scanner.min_vol = 0
    scanner.office = sector
    tickers = scanner.filtered_tickers()

    i = 0

    max_tickers = 150

    for t in tickers:
        df_ = df[df.ticker == t]
        if df_.empty or t.find(".") >= 0:
            continue

        i += 1
        if i > max_tickers:
            break
    
        chart = line_charts[chart_counter]
        chart.label = t
        chart.data = df_
        #chart.set_callback_app(app)
        chart_counter += 1

        ChartCard = [
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(chart.get_layout(),width=6),
                ])
            ])                
        ]

        chartCard = dbc.Card(
            ChartCard
        )  
        
        layout_elements.append(chartCard)

    return layout_elements


def show_filtered_pairs(minprice, maxprice, industry):
    print("SFP")
    chart_counter = 0
    filter_result = [["GNW", "OWL", 0.4], ["FITB", "NWBI", 0.1], ["TFC", "RF", 0], ["HOOD", "OWL", 0.4]]

    layout_elements = []
    #data = np.random.normal(2, 2, size=500) # replace with your own data source
    #fig = px.histogram(data, range_x=[-10, 10])
    #layout_elements.append("hist")

    #scanner = Scanner()
    scanner.min_price = minprice
    scanner.max_price = maxprice
    scanner.min_vol = 1000000
    #scanner.office = industry
    #pairs_df = scanner.get_pairs()
    filtered_pairs_df = pairs_df[(pairs_df.ratio <= 0.1) & (pairs_df.industry_title == industry)].reset_index(drop=True).sort_values(by=("ratio"), ascending=False)
    print(pairs_df)
    print(filtered_pairs_df)
    print(industry)
    i = 0

    max_tickers = 50

    #row = filtered_pairs_df.tail(1)
    #while True:
    for cols, row in filtered_pairs_df.iterrows():
        pa = row.A
        pb = row.B
        ratio = row.ratio

        print(pa, pb, ratio)
        #print(i, row)
        df_ = df[df.ticker == pa]
        dfc = df[df.ticker == pb]
        #print(df_)
        if df_.empty or pa.find(".") >= 0 or pb.find(".") >=0:
            continue

        i += 1
        if i > max_tickers:
            break
    
        chart = compare_charts[chart_counter]
        chart.chartType = "compare"
        chart.label = f"{pa} - {pb} - {ratio}"
        chart.data = df_
        chart.compareData = dfc
        chart_counter += 1

        #chart.set_callback_app(app)
        #print(df_)
        #print(dfc)

        ChartCard = [
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(chart.get_layout(),width=6),
                ])
            ])                
        ]

        chartCard = dbc.Card(
            ChartCard
        )  
        
        layout_elements.append(chartCard)

    """ for p in filter_result:
        print(p[0], p[1])
        df_ = df[df.ticker == p[0]]
        dfc = df[df.ticker == p[1]]
        if df_.empty or p[0].find(".") >= 0 or p[1].find(".") >=0:
            continue

        i += 1
        if i > max_tickers:
            break
    
        chart = compare_charts[chart_counter]
        chart.chartType = "compare"
        chart.label = f"{p[0]} - {p[1]} - {p[2]}"
        chart.data = df_
        chart.compareData = dfc
        chart_counter += 1

        #chart.set_callback_app(app)
        print(df_)
        print(dfc)

        ChartCard = [
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(chart.get_layout(),width=6),
                ])
            ])                
        ]

        chartCard = dbc.Card(
            ChartCard
        )  
        
        layout_elements.append(chartCard) """

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
        Input("industry-select", "value"),
        Input("scan-pairs", "value")
    ],
)

def apply_filter_callback(minprice, maxprice, industry, pairs):
    if minprice and maxprice and industry:
        if pairs:
            #print(sector_dropdown[int(industry)-1]["label"])
            return show_filtered_pairs(minprice, maxprice, industry_dropdown[int(industry)-1]["label"])

        else:
            
            return show_filtered_tickers(minprice, maxprice, industry_dropdown[int(industry)-1]["label"])
        
#show_filtered_pairs(10, 50, "Office of Finance")
app.run_server(debug=True, port=8060)
