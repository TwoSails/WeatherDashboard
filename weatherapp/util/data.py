"""
Scripts to get information from the database.
"""
from pymongo import MongoClient

from weatherapp.util.config import get_config
from weatherapp.util.units import data_conversion


class Data:
    def __init__(self):
        self.config = get_config()["dashboard"]
        endpoints = self.config['settings']['mongoDB']
        self.endpoints = {'windDirection': endpoints['windDirection'],
                          'avgWindSpeed': endpoints['avgWindSpeed'],
                          'recentSpeed': endpoints['recentSpeed'],
                          'windGust': endpoints['windGust'],
                          'rainfall': endpoints['rainfall'],
                          'humidity': endpoints['humidity'],
                          'pressure': endpoints['pressure'],
                          'ambientTemp': endpoints['ambientTemp'],
                          'groundTemp': endpoints['groundTemp']}

        self.data = {'windDirection': [],
                     'avgWindSpeed': [],
                     'recentSpeed': [],
                     'windGust': [],
                     'rainfall': [],
                     'humidity': [],
                     'pressure': [],
                     'ambientTemp': [],
                     'groundTemp': [],
                     'TIMESTAMPS': []}

        self.documents = None

    def all_data(self):
        sensors = self.config['sensors']
        for x in self.documents:
            if sensors['windDirection']:
                self.data['windDirection'].append(x[self.endpoints['windDirection']])
            if sensors['windSpeed']:
                self.data['avgWindSpeed'].append(x[self.endpoints['avgWindSpeed']])
            if sensors['windSpeed']:
                self.data['recentSpeed'].append(x[self.endpoints['recentSpeed']])
            if sensors['windSpeed']:
                self.data['windGust'].append(x[self.endpoints['windGust']])
            if sensors['rainfall']:
                self.data['rainfall'].append(x[self.endpoints['rainfall']])
            if sensors['humidity']:
                self.data['humidity'].append(x[self.endpoints['humidity']])
            if sensors['pressure']:
                self.data['pressure'].append(x[self.endpoints['pressure']])
            if sensors['ambientTemp']:
                self.data['ambientTemp'].append(x[self.endpoints['ambientTemp']])
            if sensors['groundTemp']:
                self.data['groundTemp'].append(x[self.endpoints['groundTemp']])
            self.data['TIMESTAMPS'].append(x['TIMESTAMP'])

        correction = [19.90498791339859, 9.370890762840645]

        humidity = [(x - correction[1]) for x in self.data['humidity']]
        self.data['humidity'] = humidity

        self.data = data_conversion(self.data)

    def endpoint_data(self):
        pass

    def get_data(self):
        PATH = self.config['settings']['mongoDBString']

        cluster = MongoClient(PATH, 27017, connect=False)

        db = cluster["weather"]
        collection = db["weatherCollection"]
        documents = []
        for x in collection.find({}):
            documents.append(x)

        self.documents = documents
