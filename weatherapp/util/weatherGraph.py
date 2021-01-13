import requests
import datetime
import os

from plotly.offline import plot
from plotly.graph_objs import Scatter


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

        self.url = self.config["settings"]["apiURL"]
        self.urlAddition = "/weather/data"

    def wind_data(self, days):
        params = {"span": int(days * 48), 'direction': True, 'speed': True, 'gust': True}
        self.dataWind = requests.get(self.url + self.urlAddition + "/wind", params=params)
        self.dataWind = self.dataWind.json()

    def wind_direction_graph(self):
        TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataWind[3]["TIMESTAMPS"][::-1]]
        windDirection = self.dataWind[1]["direction"][::-1]

        wind_direction_graph = plot([Scatter(x=TIMESTAMPS, y=windDirection, mode="lines", name="Wind Direction")],
                                    output_type="div",
                                    include_plotlyjs=False, show_link=False, link_text="")

        return wind_direction_graph

    def wind_speed_graph(self):
        TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataWind[3]["TIMESTAMPS"][::-1]]
        windSpeed = self.dataWind[0]["speed"][::-1]

        wind_speed_graph = plot([Scatter(x=TIMESTAMPS, y=windSpeed, mode="lines", name="Wind Speed")],
                                output_type="div",
                                include_plotlyjs=False, show_link=False, link_text="")

        return wind_speed_graph

    def wind_gust_graph(self):
        TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataWind[3]["TIMESTAMPS"][::-1]]
        windGust = self.dataWind[2]["gust"][::-1]

        wind_gust_graph = plot([Scatter(x=TIMESTAMPS, y=windGust, mode="lines", name="Wind Gust")],
                               output_type="div",
                               include_plotlyjs=False, show_link=False, link_text="")

        return wind_gust_graph

    def rainfall_graph(self, days):
        params = {"span": int(days * 48)}
        self.dataRainfall = requests.get(self.url + self.urlAddition + "/rainfall", params=params)
        self.dataRainfall = self.dataRainfall.json()
        TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataRainfall[1]["TIMESTAMPS"][::-1]]
        rainfall = self.dataRainfall[0]["rainfall"][::-1]

        rainfall_graph = plot([Scatter(x=TIMESTAMPS, y=rainfall, mode="lines", name="Rainfall")],
                              output_type="div",
                              include_plotlyjs=False, show_link=False, link_text="")

        return rainfall_graph

    def humidity_graph(self, days):
        params = {"span": int(days * 48)}
        self.dataHumidity = requests.get(self.url + self.urlAddition + "/humidity", params=params)
        self.dataHumidity = self.dataHumidity.json()
        TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataHumidity[1]["TIMESTAMPS"][::-1]]
        humidity = self.dataHumidity[0]["humidity"][::-1]

        humidity_graph = plot([Scatter(x=TIMESTAMPS, y=humidity, mode="lines", name="Humidity")],
                              output_type="div",
                              include_plotlyjs=False, show_link=False, link_text="")

        return humidity_graph

    def ambient_temp_graph(self, days):
        params = {"span": int(days * 48)}
        self.dataAmbientTemp = requests.get(self.url + self.urlAddition + "/temp/ambient", params=params)
        self.dataAmbientTemp = self.dataAmbientTemp.json()
        TIMESTAMPS = [datetime.datetime.fromtimestamp(x) for x in self.dataAmbientTemp[1]["TIMESTAMPS"][::-1]]
        ambientTemp = self.dataAmbientTemp[0]["ambientTemp"][::-1]

        ambient_graph = plot([Scatter(x=TIMESTAMPS, y=ambientTemp, mode="lines", name="Ambient Temp")],
                             output_type="div",
                             include_plotlyjs=False, show_link=False, link_text="")

        return ambient_graph
