import datetime

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from plotly.graph_objects import Figure
from plotly.graph_objs import Scatter, Bar, Scatterpolar
from plotly.subplots import make_subplots


class WeatherGraph:
    def __init__(self, config, page="dashboard", data=None):
        self.dataObj = data
        self.config = config[page]
        self.allData = None
        self.recentSpeed = None
        self.dataWindSpeedAvg = None
        self.dataWindDir = None
        self.dataWindGust = None
        self.dataGroundTemp = None
        self.dataAmbientTemp = None
        self.dataPressure = None
        self.dataHumidity = None
        self.dataRainfall = None
        self.dataTimestamps = None
        self.external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        self.wind_dirs = {0: "N",
                          45: "NE",
                          90: "E",
                          135: "SE",
                          180: "S",
                          225: "SW",
                          270: "W",
                          315: "NW",
                          360: "N"}

        self.degrees = [0, 45, 90, 135, 180, 225, 270, 315, 360]

    def data(self):
        data = self.dataObj
        self.recentSpeed = data.data['recentSpeed']
        self.dataWindSpeedAvg = data.data['avgWindSpeed']
        self.dataWindDir = data.data['windDirection']
        self.dataWindGust = data.data['windGust']
        self.dataGroundTemp = data.data['groundTemp']
        self.dataAmbientTemp = data.data['ambientTemp']
        self.dataPressure = data.data['pressure']
        self.dataHumidity = data.data['humidity']
        self.dataRainfall = data.data['rainfall']
        self.dataTimestamps = data.data['TIMESTAMPS']

    def wind_direction_graph(self) -> object:
        windDirectionApp = DjangoDash("windDirection")
        windDirectionApp.layout = html.Div([dcc.Graph(id="windDirectionGraph"),
                                            dcc.Slider(
                                                id="windDirectionSlider",
                                                marks={1: {'label': '1 Day'},
                                                       7: {'label': '1 Week'},
                                                       31: {'label': '1 Month'},
                                                       62: {'label': '2 Months'},
                                                       182: {'label': '6 Months'},
                                                       365: {'label': '1 year'}},
                                                max=365,
                                                min=1,
                                                value=7,
                                                step=1,
                                                updatemode='mouseup'
                                            )
                                            ])

        @windDirectionApp.callback(Output('windDirectionGraph', 'figure'), [Input('windDirectionSlider', 'value')])
        def update_figure(value):
            value *= 48
            windDirection = self.dataWindDir[::-1][:value]

            fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}, {'type': 'polar'}]])

            rSpeed = self.dataWindSpeedAvg[::-1][:value]
            rGust = self.dataWindGust[::-1][:value]
            theta = windDirection

            fig.add_trace(Scatterpolar(mode="markers", r=rSpeed, theta=theta,
                                       marker=dict(color='lightblue', size=8, symbol='square')), 1, 1)
            fig.add_trace(Scatterpolar(mode="markers", r=rGust, theta=theta,
                                       marker=dict(color='lightblue', size=8, symbol='square')), 1, 2)

            fig.update_layout(
                title="Wind Gust/Wind Average Speed in Wind Direction",
                showlegend=False,
                polar=dict(
                    radialaxis_tickfont_size=8,
                    angularaxis=dict(
                        tickfont_size=8,
                        rotation=90,  # start position of angular axis
                        direction="clockwise"
                    )
                ),
                polar2=dict(
                    radialaxis_tickfont_size=8,
                    angularaxis=dict(
                        tickfont_size=8,
                        rotation=90,
                        direction="clockwise"
                    ),
                ), transition_duration=250)
            return fig
        return None

    def wind_speed_graph(self):
        windSpeedApp = DjangoDash("windSpeed")
        windSpeedApp.layout = html.Div([dcc.Graph(id="windSpeedGraph"),
                                        dcc.Slider(
                                            id="windSpeedSlider",
                                            marks={1: {'label': '1 Day'},
                                                   7: {'label': '1 Week'},
                                                   31: {'label': '1 Month'},
                                                   62: {'label': '2 Months'},
                                                   182: {'label': '6 Months'},
                                                   365: {'label': '1 year'}},
                                            max=365,
                                            min=1,
                                            value=7,
                                            step=1,
                                            updatemode='mouseup'
                                        ), html.P(className="description-text", id='windSpeedOutput', style={"font": "Roboto"})])

        @windSpeedApp.callback(
            [Output('windSpeedGraph', 'figure'), Output('windSpeedOutput', component_property='children')],
            [Input('windSpeedSlider', 'value')])
        def update_figure(value):
            value *= 48
            TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataTimestamps[::-1][:value]]
            windSpeed = self.dataWindSpeedAvg[::-1][:value]

            fig = Figure(data=Scatter(x=TIMESTAMPS, y=windSpeed, mode="lines+markers", name="Wind Speed"))
            fig.update_layout(showlegend=False, transition_duration=250)

            return fig, f"Displaying data from {str(TIMESTAMPS[-1]).split('.')[0].replace('-', '/').replace(' ', '-')} to {str(TIMESTAMPS[0]).split('.')[0].replace('-', '/').replace(' ', '-')}"
        return None

    def wind_gust_graph(self):
        windGustApp = DjangoDash("windGust")
        windGustApp.layout = html.Div([dcc.Graph(id="windGustGraph"), dcc.Slider(
                id="windGustSlider",
                marks={1: {'label': '1 Day'},
                       7: {'label': '1 Week'},
                       31: {'label': '1 Month'},
                       62: {'label': '2 Months'},
                       182: {'label': '6 Months'},
                       365: {'label': '1 year'}},
                max=365,
                min=1,
                value=7,
                step=1,
                updatemode='mouseup'
            ), html.P(className="description-text", id='windGustOutput')])

        @windGustApp.callback([Output('windGustGraph', 'figure'), Output('windGustOutput', 'children')], [Input('windGustSlider', 'value')])
        def update_figure(value):
            value *= 48
            TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataTimestamps[::-1][:value]]
            windGust = self.dataWindGust[::-1][:value]

            fig = Figure(data=Scatter(x=TIMESTAMPS, y=windGust, mode="lines+markers", name="Wind Gust"))
            fig.update_layout(showlegend=False, transition_duration=250)

            return fig, f"Displaying data from {str(TIMESTAMPS[-1]).split('.')[0].replace('-', '/').replace(' ', '-')} to {str(TIMESTAMPS[0]).split('.')[0].replace('-', '/').replace(' ', '-')}"
        return None

    def rainfall_graph(self):
        rainfallApp = DjangoDash("rainfall")
        rainfallApp.layout = html.Div([dcc.Graph(id="rainfallGraph"),
                                       dcc.Slider(
            id="rainfallSlider",
            marks={1: {'label': '1 Day'},
                   7: {'label': '1 Week'},
                   31: {'label': '1 Month'},
                   62: {'label': '2 Months'},
                   182: {'label': '6 Months'},
                   365: {'label': '1 year'}},
            max=365,
            min=1,
            value=7,
            step=1,
            updatemode='mouseup'
        ), html.P(className="description-text", id='rainfallOutput')])

        @rainfallApp.callback([Output('rainfallGraph', 'figure'), Output('rainfallOutput', 'children')], [Input('rainfallSlider', 'value')])
        def update_figure(value):
            value *= 48

            TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataTimestamps[::-1][:value]]
            rainfall = self.dataRainfall[::-1][:value]

            fig = Figure(data=Bar(x=TIMESTAMPS, y=rainfall, name="Rainfall"))
            fig.update_layout(showlegend=False, transition_duration=250)

            return fig, f"Displaying data from {str(TIMESTAMPS[-1]).split('.')[0].replace('-', '/').replace(' ', '-')} to {str(TIMESTAMPS[0]).split('.')[0].replace('-', '/').replace(' ', '-')}"
        return None

    def humidity_graph(self):
        humidityApp = DjangoDash("humidity")
        humidityApp.layout = html.Div([dcc.Graph(id="humidityGraph"),
                                       dcc.Slider(
                                           id="humiditySlider",
                                           marks={1: {'label': '1 Day'},
                                                  7: {'label': '1 Week'},
                                                  31: {'label': '1 Month'},
                                                  62: {'label': '2 Months'},
                                                  182: {'label': '6 Months'},
                                                  365: {'label': '1 year'}},
                                           max=365,
                                           min=1,
                                           value=7,
                                           step=1,
                                           updatemode='mouseup'
                                       ), html.P(className="description-text", id='humidityOutput')])

        @humidityApp.callback([Output('humidityGraph', 'figure'), Output('humidityOutput', 'children')], [Input('humiditySlider', 'value')])
        def update_figure(value):
            value *= 48
            TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataTimestamps[::-1][:value]]
            humidity = self.dataHumidity[::-1][:value]

            fig = Figure(data=Scatter(x=TIMESTAMPS, y=humidity, mode="lines+markers", name="Humidity"))
            fig.update_layout(showlegend=False, transition_duration=250)

            return fig, f"Displaying data from {str(TIMESTAMPS[-1]).split('.')[0].replace('-', '/').replace(' ', '-')} to {str(TIMESTAMPS[0]).split('.')[0].replace('-', '/').replace(' ', '-')}"
        return None

    def ambient_temp_graph(self):
        ambientTempApp = DjangoDash("ambientTemp")
        ambientTempApp.layout = html.Div([dcc.Graph(id='tempGraph'),
                                          dcc.Slider(
                                              id="tempSlider",
                                              marks={1: {'label': '1 Day'},
                                                     7: {'label': '1 Week'},
                                                     31: {'label': '1 Month'},
                                                     62: {'label': '2 Months'},
                                                     182: {'label': '6 Months'},
                                                     365: {'label': '1 year'}},
                                              max=365,
                                              min=1,
                                              value=7,
                                              step=1,
                                              updatemode='mouseup'
                                          ), html.P(className="description-text", id='ambientOutput')])

        @ambientTempApp.callback([Output('tempGraph', 'figure'), Output('ambientOutput', 'children')], [Input('tempSlider', 'value')])
        def update_figure(value):
            value *= 48
            TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in
                          self.dataTimestamps[::-1][:value]]
            ambientTemp = self.dataAmbientTemp[::-1][:value]

            fig = Figure(data=Scatter(x=TIMESTAMPS, y=ambientTemp, mode="lines+markers", name="Ambient Temperature"))
            fig.update_layout(showlegend=False, transition_duration=250)

            return fig, f"Displaying data from {str(TIMESTAMPS[-1]).split('.')[0].replace('-', '/').replace(' ', '-')} to {str(TIMESTAMPS[0]).split('.')[0].replace('-', '/').replace(' ', '-')}"
        return None
