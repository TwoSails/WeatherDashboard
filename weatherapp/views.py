from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.cache import cache_page

from weatherapp.util.config import get_config, Sensors
from weatherapp.util.data import Data
from weatherapp.util.weather import Weather
from weatherapp.util.weatherGraph import WeatherGraph
from .forms import DataForm
from .models import Data as DataModel
from .util.export import FileExport

config = get_config()

export_name = None


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

    sensors = Sensors(config["dashboard"]["sensors"])

    data = Data()
    data.get_data()
    data.all_data()

    w = Weather(config=config, page="dashboard", data=data)
    wg = WeatherGraph(config=config, page="dashboard", data=data)

    wg.data()

    if sensors.windDirection:
        windDirection_graph = wg.wind_direction_graph()
    else:
        windDirection_graph = None

    if sensors.windSpeed:
        windSpeed_graph = wg.wind_speed_graph()
        windGust_graph = wg.wind_gust_graph()
    else:
        windSpeed_graph = None
        windGust_graph = None

    if sensors.rainfall:
        rainfall_graph = wg.rainfall_graph()
    else:
        rainfall_graph = None

    if sensors.humidity:
        humidity_graph = wg.humidity_graph()
    else:
        humidity_graph = None

    if sensors.pressure:
        pressure_graph = None
    else:
        pressure_graph = None

    if sensors.ambientTemp:
        ambientTemp_graph = wg.ambient_temp_graph()
    else:
        ambientTemp_graph = None

    if sensors.groundTemp:
        groundTemp_graph = None
    else:
        groundTemp_graph = None

    windData = w.get_wind(windDirection=sensors.windDirection, windSpeed=sensors.windSpeed)

    weather = {"windDirection": "North",
               "windSpeed": "50mph",
               "windGust": "100mph",
               "quickLookWind": {"speed": windData['speed'][-1], "direction": windData['direction'][-1],
                                 "gust": windData['gust'][-1],
                                 "recent": windData['recent'][-1]},
               "quickLookGround": w.get_ground_temp(configEntry=sensors.groundTemp)[-1],
               "quickLookAmbient": w.get_ambient_temp(configEntry=sensors.ambientTemp)[-1],
               "quickLookPressure": w.get_pressure(configEntry=sensors.pressure)[-1],
               "quickLookHumidity": w.get_humidity(configEntry=sensors.humidity)[-1],
               "quickLookRainfall": w.get_rainfall(configEntry=sensors.rainfall)[:24],
               }

    # graphs = {"rainfall": rainfall_graph}
    graphs = {'windDirection': windDirection_graph,
              'avgWindSpeed': windSpeed_graph,
              'windGust': windGust_graph,
              'rainfall': rainfall_graph,
              'humidity': humidity_graph,
              'pressure': pressure_graph,
              'ambient': ambientTemp_graph,
              'ground': groundTemp_graph}

    units = {'rainfall': config['dashboard']['settings']['units']['output']['rainfall'],
             'temp': 'C' if config['dashboard']['settings']['units']['output']['temp'] == 'celsius' else 'F',
             'speed': config['dashboard']['settings']['units']['output']['speed']}

    context = {'weather': weather, 'graphs': graphs, 'config': config, 'units': units, 'sensors': sensors.__dict__}

    print(context)

    return render(request, 'weatherapp/dashboard.html', context)


def windDirection(request):
    """unsupported"""
    return render(request, "weatherapp/direction.html")


def infoPage(request):
    return render(request, "weatherapp/info.html")


def download_page(request):
    global export_name
    if request.method == "POST":
        form = DataForm(request.POST)
        if form.is_valid():
            data = Data()
            data.get_data()
            data.all_data()
            post = get_object_or_404(DataModel)
            post.export_name = form.cleaned_data['export_name']
            post.span_int = form.cleaned_data['span_int']
            post.wind_direction = form.cleaned_data['wind_direction']
            post.avg_wind_speed = form.cleaned_data['avg_wind_speed']
            post.wind_gust = form.cleaned_data['wind_gust']
            post.rainfall = form.cleaned_data['rainfall']
            post.humidity = form.cleaned_data['humidity']
            post.ambient_temp = form.cleaned_data['ambient_temp']
            post.ground_temp = form.cleaned_data['ground_temp']
            post.pressure = form.cleaned_data['pressure']
            post.timestamps = form.cleaned_data['timestamps']
            post.save()
            fileExport = FileExport(data=data, post=post)
            fileExport.run()
            export_name = post.export_name
            # return redirect('download')
            return redirect('downloadFile')
    else:
        form = DataForm()
    return render(request, 'weatherapp/download.html', {'form': form})


def download_file_page(request):
    global export_name
    return render(request, 'weatherapp/downloadFile.html', {'export_name': export_name})


def file(request):
    content = open("weatherapp/data_files/export.json", 'r').read()
    return HttpResponse(content=content, content_type='text/json')


def handler404(request, exception):
    return render(request, '404.html')


def handler500(request):
    data = {}
    return render(request, '500.html', data)
