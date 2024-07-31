from PairTrading.frontend.charting import DashChart
from PairTrading.backend.scanner import Scanner
from PairTrading.frontend.data_utils import DataUtils as du
from PairTrading.frontend.ui_pairview import PairView
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.frontend.pair import Pair

from dash import Dash, html, dcc, Input, Output, State, ctx, ALL
import dash_bootstrap_components as dbc
import json
    
if __name__ == '__main__':
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

    scanner=Scanner()
    scanner.min_price = 5
    scanner.max_price = 70
    scanner.min_avg_vol = 500000
    scanner.industry = 'STATE COMMERCIAL BANKS'
    pairs, market_data = scanner.get_pairs()

    charts = []

    compare_charts = []
    for i in range(200):
        cchart = DashChart(f"tempcompare{i}", "compare")
        cchart.set_callback_app(app)
        compare_charts.append(cchart)

    maxcharts = 50

    for i, row in pairs.iterrows():
        if i > maxcharts:
            break

        ticker_a = row.A
        ticker_b = row.B
        avg_diff = row.avg_diff
        coint = row.coint

        # if coint > 0.2 or avg_diff > 0.2:
        #     continue

        tickera_df = market_data[market_data['ticker'] == ticker_a]
        tickerb_df = market_data[market_data['ticker'] == ticker_b]
        print(tickera_df)
        print(tickerb_df)
        comparechart = compare_charts[i]
        comparechart.chartType = "compare"

        comparechart.data = tickera_df
        comparechart.compareData = tickerb_df
        comparechart.label = f"{i}. {ticker_a} - {ticker_b} - avg_diff: {avg_diff}, coint: {coint}"
        charts.append(comparechart.get_layout()[0])

    #print(charts)

    app.layout = html.Div(
        charts
    )

    app.run_server(debug=True, port=8060)