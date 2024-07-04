from PairTrading.backend.polygon import Polygon
from PairTrading.src import _constant
from PairTrading.frontend.data_utils import DataUtils

from pprint import pprint

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

class DashChart:
    def __init__(self, name="chart", chartType="line"):
        self._data = None
        self.compareData = None
        self.chartType = chartType
        self.name = name
        self.showHeader = True
        self.showTitle = False
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

        if self.chartType == "candlestick":
            @app.callback(
                Output(f'{self.name}-graph', "figure"),
                Input(f'{self.name}-toggle-bbands', "value"))
    
            def appCallback(value):
                fig = self.chart_candlestick_callback(value)
                return fig

        elif self.chartType == "line":
            @app.callback(
                Output(f'{self.name}-graph', "figure"),
                Input(f'{self.name}-toggle-bbands', "value"),
            )
    
            def appCallback(value):
                fig = self.chart_line_callback(value)
                return fig
            
        elif self.chartType == "compare":
            @app.callback(
                Output(f'{self.name}-graph', "figure"),
                Input(f'{self.name}-toggle-normalize', "value"),
                Input(f'{self.name}-scale', "value"),
                Input(f'{self.name}-offset', "value"),
            )
    
            def appCallback(normalize, scale, offset):
                fig = self.chart_compare_callback(normalize, scale, offset)
                return fig
                 
    def get_layout(self):

        cardContent = []
        if self.showHeader:
            cardContent = [dbc.CardHeader(html.H6(self.name, className="card-title"))]

        if self.chartType == "candlestick":
            cardContent += [
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([dcc.Graph(id=f'{self.name}-graph')])
                    ]),

                    dbc.Row([
                        dbc.Col([dbc.Checklist(id=f'{self.name}-toggle-bbands', options=[{'label': 'BB', 'value': "bbands"}], value=[""], switch=True)])
                    ]) 
                ])
            ]

        elif self.chartType == "line":
            cardContent += [
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([dcc.Graph(id=f'{self.name}-graph')])
                    ]),

                    dbc.Row([
                        dbc.Col([dbc.Checklist(id=f'{self.name}-toggle-bbands', options=[{'label': 'BB', 'value': "bbands"}], value=[""], switch=True)])
                    ]) 
                ])
            ]
            
        elif self.chartType == "compare":
            cardContent += [
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([dcc.Graph(id=f'{self.name}-graph')])
                    ]),

                    dbc.Row([
                        dbc.Col([
                            dbc.Checklist(id=f'{self.name}-toggle-normalize', options=[{'label': 'Normalize', 'value': True}], value=[True], switch=True),
                            #dcc.Slider(id=f'{self.name}-scale', min=-10, max=10, value=1),
                            #dcc.Slider(id=f'{self.name}-offset', min=-10, max=10, value=0)
                            "Scale",
                            dcc.Input(id=f'{self.name}-scale', value=1, type="number", step=0.001),
                            "Offset",
                            dcc.Input(id=f'{self.name}-offset', value=0, type="number", step=0.001),
                        ])
                    ]) 
                ])
            ]
            
        

        chartCard = dbc.Card(
            cardContent
        )            
                
        layoutElements = [
            chartCard
        ]

        return layoutElements
    
    def chart_candlestick_callback(self, value):
        bbands = self.calculate_bollinger_bands(20, 2)

        figures = [
                    go.Candlestick(
                    x=self._data[self.dataKeys['Time']],
                    open=self._data[self.dataKeys['Open']],
                    high=self._data[self.dataKeys['High']],
                    low=self._data[self.dataKeys['Low']],
                    close=self._data[self.dataKeys['Close']],
                    showlegend=False)
                ] 

        if "bbands" in value:
                figures += [
                            go.Scatter(x=self._data[self.dataKeys['Time']], y=bbands['upper_band'], line={"width" : 1},showlegend=False),
                            go.Scatter(x=self._data[self.dataKeys['Time']], y=bbands['mid'], line={"width" : 1},showlegend=False),
                            go.Scatter(x=self._data[self.dataKeys['Time']], y=bbands['lower_band'], line={"width" : 1},showlegend=False) 
                    ]  
        
        fig = go.Figure(figures)

        fig.update_yaxes(
            #anchor="free",
            automargin=True,
            autorange=True
        )

        fig.update_layout(
            margin=dict(l=2, r=2, t=2, b=2),
            #title="Mega title",
            #annotations = [dict(x="2016-10-10", y=0.2, xref='x', yref='paper', showarrow=True, text="Sell here")],
            xaxis_rangeslider_visible=True,
            xaxis_rangeslider_yaxis_rangemode="auto"
        )

        return fig
    
    def chart_line_callback(self, value):

        figures = [
            go.Scatter(x=self._data[self.dataKeys['Time']], y=self._data[self.dataKeys['Close']], line_shape='linear', line={"width" : 2})
        ] 

        fig = go.Figure(figures)

        fig.update_yaxes(showgrid=True, zeroline=False, showticklabels=True, 
                 showspikes=True, spikemode='across', spikesnap='data', showline=False, spikedash='dash', spikethickness=1, spikecolor="grey", anchor="free")

        fig.update_xaxes(showgrid=True, zeroline=False, rangeslider_visible=True, showticklabels=False,
                 showspikes=True, spikemode='across', spikesnap='cursor', showline=False, spikedash='dash', spikethickness=1, spikecolor="grey")

        fig.update_layout(
            margin=dict(l=2, r=2, t=2, b=2),
            #hoverdistance=0,
            #title=self.name,
            #annotations = [dict(x="2016-10-10", y=0.2, xref='x', yref='paper', showarrow=True, text="Sell here")],
            xaxis_rangeslider_visible=True,
            #xaxis_rangeslider_yaxis_rangemode="auto"
        )

        return fig
    
    def chart_compare_callback(self, normalize, scale, offset):
        dfA = self._data
        dfB = self.compareData
        
        d = DataUtils()

        if normalize:
            dfA = d.normalize_minmax(self._data, self.dataKeys['Close'])
            dfB = d.normalize_minmax(self.compareData, self.dataKeys['Close'])
            
        dfB[self.dataKeys['Close']] = dfB[self.dataKeys['Close']] * scale + offset

        figures = [
            go.Scatter(x=self._data[self.dataKeys['Time']], y=dfA[self.dataKeys['Close']], line={"width" : 1}, name="A"),
            go.Scatter(x=self.compareData[self.dataKeys['Time']], y=dfB[self.dataKeys['Close']], line={"width" : 1},name="B"),
        ]

        fig = go.Figure(figures)

        fig.update_yaxes(
            anchor="free",
            automargin=True,
            autorange=True
        )

        fig.update_layout(
            margin=dict(l=2, r=2, t=2, b=2),
            #title=self.name,
            #annotations = [dict(x="2016-10-10", y=0.2, xref='x', yref='paper', showarrow=True, text="Sell here")],
            xaxis_rangeslider_visible=True,
            #xaxis_rangeslider_yaxis_rangemode="auto"
        )

        return fig
    
    def calculate_bollinger_bands(self, len=20, stdDev=2):
        df = pd.DataFrame()
        df[['lower_band', 'mid', 'upper_band']] = ta.bbands(self._data[self.dataKeys['Close']], length=len, std=stdDev).iloc[:, :3]
        return df

if __name__ == '__main__':

    p = Polygon()
    #print(p.list_tables())
    #tk = p.get_table("ticker_details")
    #print(p.get_table("ticker_details").columns)
    #print( tk[tk.ticker=="AAPL"].T )
    #print(p.get_table("ticker_details"))
    
    tickers = ["day_AA", "day_MSTR", "day_AU", "day_CMA", "day_DVN", "day_GCT", "day_AZEK", "day_BTI", "day_CFLT"]

    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    charts = []
    for t in tickers:
        df = p.get_table(t)
        chart = DashChart(t, "compare")
        chart.data = df
        chart.compareData = df
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

    row1 = html.Tr([
        html.Td(charts[0].get_layout()), 
        html.Td(charts[1].get_layout()),
        html.Td("")
    ])
    row2 = html.Tr([
        html.Td(charts[2].get_layout()), 
        html.Td(charts[3].get_layout()),
        html.Td("")
    ])
    row3 = html.Tr([
        html.Td(charts[4].get_layout()), 
        html.Td(charts[5].get_layout()),
        html.Td("")
    ])
    row4 = html.Tr([
        html.Td(charts[6].get_layout()), 
        html.Td(charts[7].get_layout()),
        html.Td("")
    ])
    row5 = html.Tr([
        html.Td(charts[8].get_layout())
    ])
    
    table_body = [html.Tbody([row1, row2, row3, row4, row5])]
    table = dbc.Table(table_body, borderless=True, striped=False)

    app.layout = html.Div(
        #layout_objects,
        table,
    )

    app.run_server(debug=True)

