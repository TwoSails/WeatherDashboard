import yaml
from ruamel.yaml import YAML as objYAML

from .items import change_item

DIR = "weatherapp/util/config.yml"
config_string = {'dashboard': {'settings': {'SECRET_KEY': 'YOUR SECRET KEY',
                                            'units': {'output': {'temp': 'celsius', 'speed': 'km/h', 'rainfall': 'mm'},
                                                      'input': {'temp': 'celsius', 'speed': 'km/h', 'rainfall': 'mm'}},
                                            'mongoDBString': 'raspberryweather.local',
                                            'mongoDB': {'windDirection': 'windAverage', 'recentSpeed': 'recentSpeed',
                                                        'avgWindSpeed': 'windSpeedAverage', 'windGust': 'windGust',
                                                        'rainfall': 'rainfall', 'humidity': 'humidity',
                                                        'pressure': 'pressure', 'ambientTemp': 'ambientTemp',
                                                        'groundTemp': 'groundTemp'}},
                               'quickLook': {'format': {'windDirection': 'txt'},
                                             'periods': {'windDirection': 30, 'avgWindSpeed': 360, 'windGust': 720,
                                                         'rainfall': 720, 'humidity': 30, 'pressure': 30,
                                                         'ambientTemp': 30, 'groundTemp': 30}},
                               'sensors': {'windDirection': True, 'windSpeed': True, 'rainfall': True, 'humidity': True,
                                           'pressure': True, 'ambientTemp': True, 'groundTemp': False}}}


class Config:
    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, key, dictionary[key])

    def __repr__(self):
        return f"Config: {self.__dict__}"

    def __str__(self):
        return f"Config Dict"


class Sensors:
    def __init__(self, config):
        self.windDirection = config["windDirection"]
        self.windSpeed = config["windSpeed"]
        self.rainfall = config["rainfall"]
        self.humidity = config["humidity"]
        self.pressure = config["pressure"]
        self.ambientTemp = config["ambientTemp"]
        self.groundTemp = config["groundTemp"]


def get_config():
    global DIR
    try:
        configfile = open('./weatherapp/util/config.yml', 'r')
    except FileNotFoundError:
        print("New Config File Created...")
        configfile = open(DIR, 'w')
        yaml.dump(config_string, configfile)
        configfile.close()
        configfile = open('./weatherapp/util/config.yml', 'r')
    config = yaml.safe_load(configfile.read())
    return config


def save_config(config_dict: dict):
    global DIR
    deleteme = []
    for key in config_dict.keys():
        if config_dict[key] is '' or config_dict[key] is False:
            deleteme.append(key)
    for a in deleteme:
        del config_dict[a]

    config = get_config()
    yaml = objYAML()
    file = open(DIR, 'w')
    for x in config_dict.keys():
        path = x.split('/')
        config = change_item(config, path, config_dict[x])

    yaml.dump(config, file)
    file.close()


def reset_config():
    pass
