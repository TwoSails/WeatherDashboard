import requests
import datetime
import os

from plotly.offline import plot
from plotly.graph_objs import Scatter, Bar, Scatterpolar
from plotly.graph_objects import Figure
import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots

from django_plotly_dash import DjangoDash
import plotly.graph_objects as go
from ..templatetags.wind_extra import wind_direction as windDir


class WeatherGraph:
    def __init__(self, config, page="dashboard"):
        self.config = config[page]
        self.recent = None
        self.dataWind = None
        self.dataGroundTemp = None
        self.dataAmbientTemp = None
        self.dataPressure = None
        self.dataHumidity = None
        self.dataRainfall = None

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

        self.url = self.config["settings"]["apiURL"]
        self.urlAddition = "/weather/data"

    def wind_data(self, days):
        params = {"span": int(days * 48), 'direction': True, 'speed': True, 'gust': True}
        self.dataWind = requests.get(self.url + self.urlAddition + "/wind", params=params)
        self.dataWind = self.dataWind.json()

    def wind_direction_graph(self):
        windDirection = self.dataWind[1]["direction"][::-1]

        fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'polar'}, {'type': 'polar'}]])

        rSpeed = self.dataWind[0]["speed"][::-1]
        rGust = self.dataWind[2]["gust"][::-1]
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
            ))

        windDirectionApp = DjangoDash("windDirection")
        windDirectionApp.layout = html.Div([dcc.Graph(figure=fig)])

        return None

    def wind_speed_graph(self):
        TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataWind[3]["TIMESTAMPS"][::-1]]
        windSpeed = self.dataWind[0]["speed"][::-1]

        fig = Figure(data=Scatter(x=TIMESTAMPS, y=windSpeed, mode="lines+markers", name="Wind Speed"))
        fig.update_layout(showlegend=False)

        windSpeedApp = DjangoDash("windSpeed")
        windSpeedApp.layout = html.Div([dcc.Graph(figure=fig)])

        return None

    def wind_gust_graph(self):
        TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataWind[3]["TIMESTAMPS"][::-1]]
        windGust = self.dataWind[2]["gust"][::-1]

        fig = Figure(data=Scatter(x=TIMESTAMPS, y=windGust, mode="lines+markers", name="Wind Gust"))
        fig.update_layout(showlegend=False)

        windGustApp = DjangoDash("windGust")
        windGustApp.layout = html.Div([dcc.Graph(figure=fig)])

        return None

    def rainfall_graph(self, days):
        params = {"span": int(days * 48)}
        self.dataRainfall = requests.get(self.url + self.urlAddition + "/rainfall", params=params)
        self.dataRainfall = self.dataRainfall.json()
        TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataRainfall[1]["TIMESTAMPS"][::-1]]
        rainfall = self.dataRainfall[0]["rainfall"][::-1]

        fig = Figure(data=Bar(x=TIMESTAMPS, y=rainfall, name="Rainfall"))
        fig.update_layout(showlegend=False)

        rainfallApp = DjangoDash("rainfall")
        rainfallApp.layout = html.Div([dcc.Graph(figure=fig)])

        return None

    def humidity_graph(self, days):
        params = {"span": int(days * 48)}
        self.dataHumidity = requests.get(self.url + self.urlAddition + "/humidity", params=params)
        self.dataHumidity = self.dataHumidity.json()
        TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataHumidity[1]["TIMESTAMPS"][::-1]]
        humidity = self.dataHumidity[0]["humidity"][::-1]

        fig = Figure(data=Scatter(x=TIMESTAMPS, y=humidity, mode="lines+markers", name="Humidity"))
        fig.update_layout(showlegend=False)

        humidityApp = DjangoDash("humidity")
        humidityApp.layout = html.Div([dcc.Graph(figure=fig)])

        return None

    def ambient_temp_graph(self, days):
        params = {"span": int(days * 48)}
        self.dataAmbientTemp = requests.get(self.url + self.urlAddition + "/temp/ambient", params=params)
        self.dataAmbientTemp = self.dataAmbientTemp.json()
        TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataAmbientTemp[1]["TIMESTAMPS"][::-1]]
        ambientTemp = self.dataAmbientTemp[0]["ambientTemp"][::-1]

        fig = Figure(data=Scatter(x=TIMESTAMPS, y=ambientTemp, mode="lines+markers", name="Ambient Temperature"))
        fig.update_layout(showlegend=False)

        ambientTempApp = DjangoDash("ambientTemp")
        ambientTempApp.layout = html.Div([dcc.Graph(figure=fig)])

        return None
