
from PairTrading.backend.data_wrangler import DataWrangler
from PairTrading.frontend.pair import Pair
from PairTrading.backend.scanner import Scanner
from PairTrading.frontend.ui_scannerview import ScannerView
from PairTrading.frontend.ui_pairview import PairView

from dash import Dash, html, dcc, Input, Output 
import dash_bootstrap_components as dbc  

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

scanner=Scanner()

#Scanner view
scanner.min_price = 2
scanner.max_price = 200
scanner.min_vol = 100000
scanner_view = ScannerView(scanner)
scanner_view.set_callback_app(app)

#Pair View
pair_view = PairView("LNT", "WEC")
pair_view.market_data = scanner.all_market_data
pair_view.set_callback_app(app)

tab1_content = dbc.Card(
    dbc.CardBody(
            scanner_view.get_layout(),
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
            pair_view.get_layout(),
    ),
    className="mt-3",
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Scanner View"),
        dbc.Tab(tab2_content, label="Pair View"),
        #dbc.Tab("This tab's content is never seen", label="Tab 3", disabled=True),
    ]
)

app.layout = html.Div(tabs)

app.run_server(debug=True, port=8060)