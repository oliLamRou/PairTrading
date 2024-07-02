from PairTrading.backend.polygon import Polygon
from PairTrading.src import _constant

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
    def __init__(self, name="chart", chartType="line"):
        self._data = None
        self.chartType = chartType
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
    
        def appCallbackA(value):
            fig = chart.chart_line_callback(df, value, self.name)
            return fig
        
        """ if self.chartType == "candlestick":
            @app.callback(
                Output(f'{self.name}-graph', "figure"),
                Input(f'{self.name}-toggle-bbands', "value"))
    
            def appCallbackA(value):
                fig = chart.chart_candlestick_callback(df, value, self.name)
                return fig

        elif self.chartType == "line":
            @app.callback(
                Output(f'{self.name}-graph', "figure"),
                Input(f'{self.name}-toggle-bbands', "value"))
    
            def appCallbackB(value):
                fig = chart.chart_line_callback(df, value, self.name)
                return fig """
                 
    def get_layout(self):

        layoutElements = [
            html.H6(f'{self.name} stock candlestick chart'),
            dcc.Markdown(self.name),
            dcc.Checklist(id=f'{self.name}-toggle-bbands', options=[{'label': 'Show Bollinger Bands', 'value': "bbands"}], value=["bbands"]),
            #dcc.Input(id=f'{self.name}-bbands-length', value=20, type="number", step=1), "length",
            #dcc.Input(id=f'{self.name}-bbands-stdDev', value=2, type="number", step=1), "steps",
            dcc.Graph(id=f'{self.name}-graph')
        ]
        return layoutElements

        if self.chartType == "candlestick":
            layoutElements += [
                dcc.Checklist(id=f'{self.name}-toggle-bbands', options=[{'label': 'Show Bollinger Bands', 'value': "bbands"}], value=["bbands"]),
                #dcc.Input(id=f'{self.name}-bbands-length', value=20, type="number", step=1), "length",
                #dcc.Input(id=f'{self.name}-bbands-stdDev', value=2, type="number", step=1), "steps",
                dcc.Graph(id=f'{self.name}-graph')
            ]

        elif self.chartType == "line":
            layoutElements += [
                dcc.Checklist(id=f'{self.name}-toggle-bbands', options=[{'label': 'Show Bollinger Bands', 'value': "bbands"}], value=["bbands"]),
                #dcc.Input(id=f'{self.name}-bbands-length', value=20, type="number", step=1), "length",
                #dcc.Input(id=f'{self.name}-bbands-stdDev', value=2, type="number", step=1), "steps",
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
                            go.Scatter(x=df[self.dataKeys['Time']], y=bbands['upper_band'], line={"width" : 1}),
                            go.Scatter(x=df[self.dataKeys['Time']], y=bbands['mid'], line={"width" : 1}),
                            go.Scatter(x=df[self.dataKeys['Time']], y=bbands['lower_band'], line={"width" : 1}) 
                    ]  
        
        fig = go.Figure(figures)

        fig.update_yaxes(
            #anchor="free",
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
    
    def chart_line_callback(self, df, value, name='',):
        #bbands = self.calculate_bollinger_bands(df, 20, 2)

        figures = [
            go.Scatter(x=self._data[self.dataKeys['Time']], y=self._data[self.dataKeys['Close']], line={"width" : 1})
        ] 

        fig = go.Figure(figures)

        fig.update_yaxes(
            #anchor="free",
            automargin=True,
            autorange=True
        )

        fig.update_layout(
            title=name,
            #annotations = [dict(x="2016-10-10", y=0.2, xref='x', yref='paper', showarrow=True, text="Sell here")],
            xaxis_rangeslider_visible=True,
            #xaxis_rangeslider_yaxis_rangemode="auto"
        )
        print(df)
        return fig
    
    def calculate_bollinger_bands(self, df, len=20, stdDev=2):
        df[['lower_band', 'mid', 'upper_band']] = ta.bbands(df[self.dataKeys['Close']], length=len, std=stdDev).iloc[:, :3]
        return df

if __name__ == '__main__':

    p = Polygon()

    #print(p.list_tables())
    print("AA", p.get_table("day_AA"))
    print("MSTR", p.get_table("day_MSTR"))
    #tickers = ["day_AA", "day_MSTR", "day_AU", "day_CMA", "day_DVN"]
    
    tickers = ["day_DVN", "day_MSTR"]

    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    charts = []
    for t in tickers:
        df = p.get_table(t)
        chart = Charting(t, "lines")
        chart.data = df
        chart.dataKeys = {
            "Time" : _constant.HISTORICAL_COLUMNS['t'][0], 
            "Open" : _constant.HISTORICAL_COLUMNS['o'][0],
            "Close" : _constant.HISTORICAL_COLUMNS['c'][0], 
            "High" : _constant.HISTORICAL_COLUMNS['h'][0], 
            "Low" : _constant.HISTORICAL_COLUMNS['l'][0]
        }
        
        chart.set_callback_app(app)
        charts.append(chart)

    layout_objects = []
    for c in charts:
        #layout_objects += c.chart_candlestick()
        layout_objects += c.get_layout()

    app.layout = html.Div(
        layout_objects,
    )

    app.run_server(debug=True)

