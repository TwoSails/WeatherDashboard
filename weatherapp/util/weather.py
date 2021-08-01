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

    @lru_cache(maxsize=12)
    def get_wind(self, windDirection: bool = True, windSpeed: bool = True) -> dict:
        span = int(self.config["quickLook"]["periods"]["windGust"] / 30)
        returned = {}
        if windDirection:
            returned['direction'] = self.dataObj.data["windDirection"][span:]
        else:
            returned['direction'] = [None]

        if windSpeed:
            returned['recent'] = self.dataObj.data['recentSpeed'][span:]
            returned['speed'] = self.dataObj.data['avgWindSpeed'][span:]
            returned['gust'] = self.dataObj.data['windGust'][span:]
        else:
            returned['recent'] = [None]
            returned['speed'] = [None]
            returned['gust'] = [None]

        if windDirection or windSpeed:
            returned['TIMESTAMP'] = self.dataObj.data['TIMESTAMPS'][span:]
        else:
            returned['TIMESTAMP'] = [None]

        return returned

    @lru_cache(maxsize=12)
    def get_ground_temp(self, configEntry: bool = True) -> list:
        if configEntry:
            span = int(self.config["quickLook"]["periods"]["groundTemp"] / 30)
            return self.dataObj.data['groundTemp'][span:]
        else:
            return [None]

    @lru_cache(maxsize=12)
    def get_ambient_temp(self, configEntry: bool = True) -> list:
        if configEntry:
            span = int(self.config["quickLook"]["periods"]["ambientTemp"] / 30)
            return self.dataObj.data['ambientTemp'][span:]
        else:
            return [None]

    @lru_cache(maxsize=12)
    def get_pressure(self, configEntry: bool = True) -> list:
        if configEntry:
            span = int(self.config["quickLook"]["periods"]["pressure"] / 30)
            return self.dataObj.data['pressure'][span:]
        else:
            return [None]

    @lru_cache(maxsize=12)
    def get_humidity(self, configEntry: bool = True) -> list:
        if configEntry:
            span = int(self.config["quickLook"]["periods"]["humidity"] / 30)
            return self.dataObj.data['humidity'][span:]
        else:
            return [None]

    @lru_cache(maxsize=12)
    def get_rainfall(self, configEntry: bool = True) -> list:
        if configEntry:
            span = int(self.config["quickLook"]["periods"]["rainfall"] / 30)
            return self.dataObj.data['rainfall'][-span:]
        else:
            return [None for x in range(30)]
