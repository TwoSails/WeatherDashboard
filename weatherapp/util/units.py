from weatherapp.util.config import get_config
from weatherapp.util.convert import *

configFile = get_config()['dashboard']


def compare():
    global configFile
    config = configFile
    config = config['settings']['units']
    outputs = config['output']
    inputs = config['input']
    if outputs['temp'] == inputs['temp']:
        tempSame = True
    else:
        tempSame = False
    if outputs['speed'] == inputs['speed']:
        speedSame = True
    else:
        speedSame = False
    if outputs['rainfall'] == inputs['rainfall']:
        rainfallSame = True
    else:
        rainfallSame = False
    return tempSame, speedSame, rainfallSame


def data_conversion(data):
    tempSame, speedSame, rainfallSame = compare()
    global configFile
    config = configFile
    sensors = config['sensors']
    dataset = {'windDirection': data['windDirection'],
               'recentSpeed': [],
               'avgWindSpeed': [],
               'windGust': [],
               'rainfall': [],
               'humidity': data['humidity'],
               'pressure': data['pressure'],
               'ambientTemp': [],
               'groundTemp': [],
               'TIMESTAMPS': data['TIMESTAMPS']}

    if not tempSame:
        if sensors['ambientTemp']:
            unitToGo = config['settings']['units']['output']['temp']
            if unitToGo == 'celsius':
                for x in data['ambientTemp']:
                    dataset['ambientTemp'].append(fahrenheit_to_celsius(x))
            else:
                for x in data['ambientTemp']:
                    dataset['ambientTemp'].append(celsius_to_fahrenheit(x))
        else:
            dataset['ambientTemp'] = data['ambientTemp']

        if sensors['groundTemp']:
            unitToGo = config['settings']['units']['output']['temp']
            if unitToGo == 'celsius':
                for x in data['groundTemp']:
                    dataset['groundTemp'].append(fahrenheit_to_celsius(x))
            else:
                for x in data['groundTemp']:
                    dataset['groundTemp'].append(celsius_to_fahrenheit(x))
        else:
            dataset['groundTemp'] = data['groundTemp']
    else:
        dataset['ambientTemp'] = data['ambientTemp']
        dataset['groundTemp'] = data['groundTemp']

    if not rainfallSame:
        if sensors['rainfall']:
            unitToGo = config['settings']['units']['output']['rainfall']
            if unitToGo == 'mm':
                for x in data['rainfall']:
                    dataset['rainfall'].append(inches_to_mm(x))
                    print('inches to mm')
            else:
                for x in data['rainfall']:
                    dataset['rainfall'].append(mm_to_inches(x))
    else:
        dataset['rainfall'] = data['rainfall']

    if not speedSame:
        if sensors['windSpeed']:
            unitToGo = config['settings']['units']['output']['speed']
            if unitToGo == 'km/h':
                for x in data['recentSpeed']:
                    dataset['recentSpeed'].append(mph_to_kmh(x))
            else:
                for x in data['recentSpeed']:
                    dataset['recentSpeed'].append(kmh_to_mph(x))
        else:
            dataset['recentSpeed'] = data['recentSpeed']

        if sensors['windSpeed']:
            unitToGo = config['settings']['units']['output']['speed']
            if unitToGo == 'km/h':
                for x in data['avgWindSpeed']:
                    dataset['avgWindSpeed'].append(mph_to_kmh(x))
            else:
                for x in data['avgWindSpeed']:
                    dataset['avgWindSpeed'].append(kmh_to_mph(x))
        else:
            dataset['avgWindSpeed'] = data['avgWindSpeed']

        if sensors['windSpeed']:
            unitToGo = config['settings']['units']['output']['speed']
            if unitToGo == 'km/h':
                for x in data['windGust']:
                    dataset['windGust'].append(mph_to_kmh(x))
            else:
                for x in data['windGust']:
                    dataset['windGust'].append(kmh_to_mph(x))
        else:
            dataset['windGust'] = data['windGust']
    else:
        dataset['recentSpeed'] = data['recentSpeed']
        dataset['avgWindSpeed'] = data['avgWindSpeed']
        dataset['windGust'] = data['windGust']

    return dataset
