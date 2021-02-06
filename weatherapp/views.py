from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.cache import cache_page

from weatherapp.util.weather import Weather
from weatherapp.util.weatherGraph import WeatherGraph
from weatherapp.util.config import get_config

from plotly.offline import plot
from plotly.graph_objs import Scatter

from functools import lru_cache

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
    w = Weather(config=config, page="dashboard")
    wg = WeatherGraph(config=config, page="dashboard")

    wg.data()

    windDirection_graph = wg.wind_direction_graph()
    windSpeed_graph = wg.wind_speed_graph()
    windGust_graph = wg.wind_gust_graph()
    rainfall_graph = wg.rainfall_graph()
    humidity_graph = wg.humidity_graph()
    ambient_graph = wg.ambient_temp_graph()

    windData = w.get_wind()
    ambientData = w.get_ambient_temp()[0]["ambientTemp"]
    humidityData = w.get_humidity()[0]["humidity"]

    weather = {"windDirection": "North",
               "windSpeed": "50mph",
               "windGust": "100mph",
               "quickLookWind": {"speed": windData[0], "direction": windData[1], "gust": windData[2],
                                 "recent": windData[3]},
               "quickLookGround": w.get_ground_temp()[0],
               "quickLookAmbient": ambientData[len(ambientData) - 1],
               "quickLookPressure": w.get_pressure()[0],
               "quickLookHumidity": humidityData[len(humidityData) - 1],
               "quickLookRainfall": w.get_rainfall()[0],
               }

    # graphs = {"rainfall": rainfall_graph}
    graphs = {'windDirection': windDirection_graph,
              'avgWindSpeed': windSpeed_graph,
              'windGust': windGust_graph,
              'rainfall': rainfall_graph,
              'humidity': humidity_graph,
              'ambient': ambient_graph}

    context = {'weather': weather, 'graphs': graphs, 'config': config}

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
