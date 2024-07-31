from PairTrading.frontend.data_utils import DataUtils
import pandas as pd
import pandas_ta as ta
import plotly.graph_objects as go
import time

from dash import Dash, html, dcc, Input, Output, ctx 
import dash_bootstrap_components as dbc


class DashChart:
    def __init__(self, name="chart", chartType="line"):
        self._data = None
        self.markers_df = pd.DataFrame()
        self.name = name
        self.label = "Label 1"
        self.showHeader = True
        self.showTitle = False
        self.dataKeys = {"Time" : "date", "Open" : "open", "Close" : "close", "High" : "high", "Low" : "low"}
        self.compareData = None
        self.chartType = chartType
        
        #default callback inputs
        if self.chartType == "candlestick":
            self.callback_inputs = [Input(f'{self.name}-toggle-bbands', "value")]
            #self.callback_inputs.append(Input('interval-component', 'n_intervals'))

        elif self.chartType == "line":
            self.callback_inputs = [Input(f'{self.name}-toggle-bbands', "value")]
            
        elif self.chartType == "compare":
            self.callback_inputs = [
                Input(f'{self.name}-toggle-normalize', "value"),
                Input(f'{self.name}-scale', "value"),
                Input(f'{self.name}-offset', "value")
            ]

        #append callback functions
        self.pre_callback_functions = []
        self.post_callback_functions = []

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
            self.callback_inputs,
        )
        def appCallback(*args):
            # print(self.callback_inputs)
            # print(ctx.inputs_list)

            #Execute Pre-callbacks
            for f in self.pre_callback_functions:
                f()

            #Callbacks
            if self.chartType == "candlestick":
                show_bbands = [item["value"] for item in ctx.inputs_list if item["id"] == f'{self.name}-toggle-bbands'][0]
                fig = self.chart_candlestick_callback(show_bbands)

            elif self.chartType == "line":
                fig = self.chart_line_callback(args)

            elif self.chartType == "compare":
                normalize = [item["value"] for item in ctx.inputs_list if item["id"] == f'{self.name}-toggle-normalize'][0]
                scale = [item["value"] for item in ctx.inputs_list if item["id"] == f'{self.name}-scale'][0]
                offset = [item["value"] for item in ctx.inputs_list if item["id"] == f'{self.name}-offset'][0]

                fig = self.chart_compare_callback(normalize, scale, offset)
            
            #Execute post-callbacks
            for f in self.post_callback_functions:
                f()

            return fig
    
    def chart_candlestick_callback(self, value):
        bbands = self.calculate_bollinger_bands(18, 2)        
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
            anchor="free",
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
            go.Scatter(x=self._data[self.dataKeys['Time']], y=self._data[self.dataKeys['Close']], line_shape='linear', line={"width" : 2}),
            #go.Scatter(mode="markers", x=self.markers_df["time"], y=self.markers_df["price"]),
        ] 

        fig = go.Figure(figures)
        fig.update_traces(
            marker=dict(size=8, symbol="diamond", line=dict(width=2, color="DarkSlateGrey")),
            selector=dict(mode="markers"),
)

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
        yaxis = self.dataKeys['Close']
        
        if normalize:
            pd.options.mode.copy_on_write = True
            self._data["normalized_close"] = DataUtils.normalize_minmax(self._data[self.dataKeys['Close']])
            self.compareData["normalized_close"] = DataUtils.normalize_minmax(self.compareData[self.dataKeys['Close']])
            yaxis = "normalized_close"

        else:
            yaxis = "scaled_close"
            self._data["scaled_close"] = self._data[self.dataKeys['Close']]
            self.compareData["scaled_close"] = self.compareData[self.dataKeys['Close']] * scale + offset

        figures = [
            go.Scatter(x=self._data[self.dataKeys['Time']], y=self._data[yaxis], line={"width" : 1}, name="A"),
            go.Scatter(x=self.compareData[self.dataKeys['Time']], y=self.compareData[yaxis], line={"width" : 1},name="B"),
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
    
    def get_layout(self):
        cardContent = []
        if self.showHeader:
            cardContent = [dbc.CardHeader(html.H6(self.label, className="card-title"))]
        
        if self.chartType == "candlestick":
            cardContent += [
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id=f'{self.name}-graph'),
                            dcc.Interval(
                            id='interval-component',
                            interval=0.5*1000,  # in milliseconds
                            n_intervals=0
                            ),
                            dcc.Store(id='trigger-update', data=0)
                        ]),
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

if __name__ == '__main__':
    from PairTrading.backend.scanner import Scanner
    import numpy as np
    import random
    from threading import Thread
    import time

    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

    scanner=Scanner()
    scanner.min_price = 5
    scanner.max_price = 70
    scanner.min_avg_vol = 500000
    scanner.industry = 'STATE COMMERCIAL BANKS'

    ticker_a = "AWR"
    ticker_b = "MSEX"
    market_data = scanner.market_data([ticker_a, ticker_b])

    cchart = DashChart(f"cchart", "candlestick")
    cchart.set_callback_app(app)

    data_df = pd.DataFrame()

    def gen_rand_data():
        while True:
            print("gen data")
            data = []
            for i in range(100):
                d = {"date" : i, "open" : random.randrange(2,5), "close" : random.randrange(5,7), "high" : random.randrange(0,5), "low" : random.randrange(5,10)}
                data.append(d)
            global data_df
            data_df = pd.DataFrame(data)
            update_chart_data(data_df)
            time.sleep(0.2)

    def update_chart_data(data):
        cchart.data = data
    
    #thread = Thread(target=gen_rand_data)
    #thread.start()
    
    tickera_df = market_data[market_data['ticker'] == ticker_a]

    cchart.label = "Test Chart"

    app.layout = html.Div(
        cchart.get_layout()
    )

    app.run_server(debug=True, port=8060)
