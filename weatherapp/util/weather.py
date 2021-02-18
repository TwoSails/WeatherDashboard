import requests
from functools import lru_cache


class Weather:
    def __init__(self, config=None, page="dashboard", data=None):
        self.dataObj = data
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
        span = int(self.config["quickLook"]["periods"]["windGust"] / 30)
        if configEntry:
            return {'recent': self.dataObj.data['recentSpeed'][span:],
                    'speed': self.dataObj.data['avgWindSpeed'][span:],
                    'gust': self.dataObj.data['windGust'][span:],
                    'direction': self.dataObj.data['windDirection'][span:],
                    'TIMESTAMP': self.dataObj.data['TIMESTAMPS'][span:]}
        else:
            return None

    @lru_cache(maxsize=12)
    def get_ground_temp(self, configEntry=True):
        if configEntry:
            span = int(self.config["quickLook"]["periods"]["groundTemp"] / 30)
            return {'groundTemp': self.dataObj.data['groundTemp'][span:]}
        else:
            return None

    @lru_cache(maxsize=12)
    def get_ambient_temp(self, configEntry=True):
        if configEntry:
            span = int(self.config["quickLook"]["periods"]["ambientTemp"] / 30)
            return {'ambientTemp': self.dataObj.data['ambientTemp'][span:]}
        else:
            return None

    @lru_cache(maxsize=12)
    def get_pressure(self, configEntry=True):
        if configEntry:
            span = int(self.config["quickLook"]["periods"]["pressure"] / 30)
            return {'pressure': self.dataObj.data['pressure'][span:]}
        else:
            return None

    @lru_cache(maxsize=12)
    def get_humidity(self, configEntry=True):
        if configEntry:
            span = int(self.config["quickLook"]["periods"]["humidity"] / 30)
            return {'humidity': self.dataObj.data['humidity'][span:]}
        else:
            return None

    @lru_cache(maxsize=12)
    def get_rainfall(self, configEntry=True):
        if configEntry:
            span = int(self.config["quickLook"]["periods"]["rainfall"] / 30)
            return {'rainfall': self.dataObj.data['rainfall'][-span:]}
