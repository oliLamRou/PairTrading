import sys
import matplotlib.pyplot as plt
import pandas as pd
import pandas_ta as ta
import seaborn as sb
import plotly.graph_objects as go

from dash import Dash, html, dcc, Input, Output  # pip install dash
import plotly.express as px
import dash_ag_grid as dag
import dash_bootstrap_components as dbc   # pip install dash-bootstrap-components

import matplotlib      # pip install matplotlib
#matplotlib.use('agg')
import base64
from io import BytesIO


class Charting:
    def __init__(self, name):
        self._data = None
        self.name = name
        self.dataKeys = {"Time" : "Time", "Open" : "Open", "Close" : "Close", "High" : "High", "Low" : "Low"}

    @property
    def data(self):
        if not self._data:
            self._data = []

        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def set_callback_app(self, app):
        @app.callback(
        Output(f'{self.name}-graph', "figure"),
        Input(f'{self.name}-toggle-bbands', "value"))
    
        def appCallback(value):

            df = self._data
            fig = chart.chart_candlestick_callback(df, value, self.name)
        
            return fig
          
    def chart_candlestick(self):
        layoutElements = [
            html.H6(f'{self.name} stock candlestick chart'),
            dcc.Checklist(id=f'{self.name}-toggle-bbands', options=[{'label': 'Show Bollinger Bands', 'value': "bbands"}], value=["bbands"]),
            dcc.Input(id=f'{self.name}-bbands-length', value=20, type="number", step=1), "length",
            dcc.Input(id=f'{self.name}-bbands-stdDev', value=2, type="number", step=1), "steps",
            dcc.Graph(id=f'{self.name}-graph')
        ]

        return layoutElements
    
    def chart_candlestick_callback(self, df, value, name='',):
        bbands = self.calculate_bollinger_bands(df, 20, 2)

        figures = [
                    go.Candlestick(
                    x=df[self.dataKeys['Time']],
                    open=df[self.dataKeys['Open']],
                    high=df[self.dataKeys['High']],
                    low=df[self.dataKeys['Low']],
                    close=df[self.dataKeys['Close']])
                ] 
        
        if "bbands" in value:
                figures += [
                            go.Scatter(x=df['Date'], y=bbands['upper_band'], line={"width" : 1}),
                            go.Scatter(x=df['Date'], y=bbands['mid'], line={"width" : 1}),
                            go.Scatter(x=df['Date'], y=bbands['lower_band'], line={"width" : 1}) 
                    ]  
        
        fig = go.Figure(figures)

        fig.update_yaxes(
            anchor="free",
            automargin=True,
            autorange=True
        )

        fig.update_layout(
            title="Mega title",
            #annotations = [dict(x="2016-10-10", y=0.2, xref='x', yref='paper', showarrow=True, text="Sell here")],
            xaxis_rangeslider_visible=True,
            xaxis_rangeslider_yaxis_rangemode="auto"
        )

        return fig
    
    def calculate_bollinger_bands(self, df, len=20, stdDev=2):
        df[['lower_band', 'mid', 'upper_band']] = ta.bbands(df['Close'], length=len, std=stdDev).iloc[:, :3]
        return df

if __name__ == '__main__':
    if sys.platform.startswith("win"):
        dataPath = "D:\\Trading\\Dev\\branch scanner\\PairTrading\\data\\historical\\"

    elif sys.platform == "darwin":
        dataPath = "/Users/gab/Documents/Trading/data/"
    
    tickers = ["AA", "AAPL", "ACM", "AU", "CMA", "DVN"]

    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    charts = []
    for t in tickers:
        chart = Charting(t)
        chart.data = pd.read_csv(f'{dataPath}{t}.csv')
        chart.dataKeys = {"Time" : "Date", "Open" : "Open", "Close" : "Close", "High" : "High", "Low" : "Low"}
        chart.set_callback_app(app)
        charts.append(chart)

    layout_objects = []
    for c in charts:
        layout_objects += c.chart_candlestick()

    app.layout = html.Div(
        layout_objects,
    )

    app.run_server(debug=True)

