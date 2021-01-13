import requests
from functools import lru_cache


class Weather:
    def __init__(self, config=None, page="dashboard"):
        self.recent = None
        self.dataWind = None
        self.dataGroundTemp = None
        self.dataAmbientTemp = None
        self.dataPressure = None
        self.dataHumidity = None
        self.dataRainfall = None

        self.config = config[page]

        self.url = self.config["settings"]["apiURL"]
        self.urlAddition = "/weather/data"

    @lru_cache(maxsize=12)
    def get_wind(self, configEntry=True):
        params = {"speed": True, "recent": True, "gust": True, "direction": True}
        if configEntry:
            params["span"] = int(self.config["quickLook"]["periods"]["windGust"] / 30)
        self.dataWind = requests.get(self.url + "/weather/data/wind", params=params)
        return self.dataWind.json()

    @lru_cache(maxsize=12)
    def get_ground_temp(self, configEntry=True):
        params = {}
        if configEntry:
            params["span"] = int(self.config["quickLook"]["periods"]["groundTemp"] / 30)
        self.dataGroundTemp = requests.get(self.url + self.urlAddition + "/temp/ground", params=params)
        return self.dataGroundTemp.json()

    @lru_cache(maxsize=12)
    def get_ambient_temp(self, configEntry=True):
        params = {}
        if configEntry:
            params["span"] = int(self.config["quickLook"]["periods"]["ambientTemp"] / 30)
        self.dataAmbientTemp = requests.get(self.url + self.urlAddition + "/temp/ambient", params=params)
        return self.dataAmbientTemp.json()

    @lru_cache(maxsize=12)
    def get_pressure(self, configEntry=True):
        params = {}
        if configEntry:
            params["span"] = int(self.config["quickLook"]["periods"]["pressure"] / 30)
        self.dataPressure = requests.get(self.url + self.urlAddition + "/pressure", params=params)
        return self.dataPressure.json()

    @lru_cache(maxsize=12)
    def get_humidity(self, configEntry=True):
        params = {}
        if configEntry:
            params["span"] = int(self.config["quickLook"]["periods"]["humidity"] / 30)
        self.dataHumidity = requests.get(self.url + self.urlAddition + "/humidity", params=params)
        return self.dataHumidity.json()

    @lru_cache(maxsize=12)
    def get_rainfall(self, configEntry=True):
        params = {}
        if configEntry:
            params["span"] = int(self.config["quickLook"]["periods"]["rainfall"] / 30)
        self.dataRainfall = requests.get(self.url + self.urlAddition + "/rainfall", params=params)
        return self.dataRainfall.json()

