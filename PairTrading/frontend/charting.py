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
            #prevent_initial_call='initial_duplicate'
        )
        def appCallback(*args):
            print(ctx.inputs_list)

            for f in self.pre_callback_functions:
                f()

            #time.sleep(0.8)

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

            for f in self.post_callback_functions:
                f()

            return fig
    
    def chart_candlestick_callback(self, value):
        print("chart_candlestick_callback")
        #print(self._data)
        bbands = self.calculate_bollinger_bands(17, 3)
        
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
                        dbc.Col([dcc.Graph(id=f'{self.name}-graph')]),
                        dcc.Interval(
                            id='interval-component',
                            interval=1*1000,  # in milliseconds
                            n_intervals=0
                        )
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

if __name__ == '__main__':

    from PairTrading.backend.data_wrangler import DataWrangler
    dw = DataWrangler()
    df = dw._DataWrangler__polygon_db.get_table('market_data')

    tickers = ["AA", "MSTR", "AU", "CMA", "DVN", "GCT", "AZEK", "BTI", "CFLT"]

    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    charts = []
    for t in tickers:
        chart = DashChart(t, "line")
        chart.label = t
        print(df[df.ticker == t])
        chart.data = df[df.ticker == t]
        
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

