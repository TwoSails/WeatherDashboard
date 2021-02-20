from django.shortcuts import render
from django.views.decorators.cache import cache_page

from weatherapp.util.config import get_config
from weatherapp.util.data import Data
from weatherapp.util.weather import Weather
from weatherapp.util.weatherGraph import WeatherGraph

config = get_config()


# Create your views here.
def index(request):
    weather = {
        "city": 'Hello World!',
        "temperature": "/None/",
        "description": "This is a test for the website! It is to make sure that it is set up correctly"
    }

    context = {'weather': weather}

    return render(request, 'weatherapp/index.html', context)


cache_page(200)


def dashboard(request):
    global config

    data = Data()
    data.get_data()
    data.all_data()

    w = Weather(config=config, page="dashboard", data=data)
    wg = WeatherGraph(config=config, page="dashboard", data=data)

    wg.data()

    windDirection_graph = wg.wind_direction_graph()
    windSpeed_graph = wg.wind_speed_graph()
    windGust_graph = wg.wind_gust_graph()
    rainfall_graph = wg.rainfall_graph()
    humidity_graph = wg.humidity_graph()
    ambient_graph = wg.ambient_temp_graph()

    windData = w.get_wind()

    weather = {"windDirection": "North",
               "windSpeed": "50mph",
               "windGust": "100mph",
               "quickLookWind": {"speed": windData['speed'][-1], "direction": windData['direction'][-1], "gust": windData['gust'][-1],
                                 "recent": windData['recent'][-1]},
               "quickLookGround": w.get_ground_temp()['groundTemp'],
               "quickLookAmbient": w.get_ambient_temp()['ambientTemp'][-1],
               "quickLookPressure": w.get_pressure()['pressure'],
               "quickLookHumidity": w.get_humidity()['humidity'][-1],
               "quickLookRainfall": w.get_rainfall()['rainfall'][:24],
               }

    # graphs = {"rainfall": rainfall_graph}
    graphs = {'windDirection': windDirection_graph,
              'avgWindSpeed': windSpeed_graph,
              'windGust': windGust_graph,
              'rainfall': rainfall_graph,
              'humidity': humidity_graph,
              'ambient': ambient_graph}

    units = {'rainfall': config['dashboard']['settings']['units']['output']['rainfall'],
             'temp': 'C' if config['dashboard']['settings']['units']['output']['temp'] == 'celsius' else 'F',
             'speed': config['dashboard']['settings']['units']['output']['speed']}

    context = {'weather': weather, 'graphs': graphs, 'config': config, 'units': units}

    return render(request, 'weatherapp/dashboard.html', context)


def windDirection(request):
    """unsupported"""
    return render(request, "weatherapp/direction.html")


def infoPage(request):
    return render(request, "weatherapp/info.html")


def handler404(request, exception):
    return render(request, '404.html')


def handler500(request):
    data = {}
    return render(request, '500.html', data)
