from django.contrib import admin
from django.contrib.admin import AdminSite
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy

from .forms import ConfigForm
from .models import Data
from .util.config import get_config, save_config


class Admin(AdminSite):
    site_title = ugettext_lazy('Weather Dashboard Admin')
    site_header = ugettext_lazy('Weather Dashboard Admin')
    index_title = ugettext_lazy('Weather Dashboard Admin')


class DataAdmin(admin.ModelAdmin):
    list_display = (
        'export_name', 'span_int', 'wind_direction', 'avg_wind_speed', 'wind_gust', 'rainfall', 'humidity',
        'ambient_temp', 'ground_temp', 'pressure', 'timestamps')


def settings(request):
    if request.method == "GET":
        form = ConfigForm(request.GET)
        formDict = {}
        if form.is_valid():
            formDict['dashboard/settings/units/output/temp'] = request.GET['units_output_temp']
            formDict['dashboard/settings/units/output/speed'] = request.GET['units_output_speed']
            formDict['dashboard/settings/units/output/rainfall'] = request.GET['units_output_rainfall']
            formDict['dashboard/settings/units/input/temp'] = request.GET['units_input_temp']
            formDict['dashboard/settings/units/input/speed'] = request.GET['units_input_speed']
            formDict['dashboard/settings/units/input/rainfall'] = request.GET['units_input_rainfall']

            formDict['dashboard/settings/mongoDBString'] = request.GET['mongoDB_string']
            formDict['dashboard/settings/mongoDB/windDirection'] = request.GET['mongoDB_wind_direction']
            formDict['dashboard/settings/mongoDB/recentSpeed'] = request.GET['mongoDB_recent_speed']
            formDict['dashboard/settings/mongoDB/avgWindSpeed'] = request.GET['mongoDB_avg_wind_speed']
            formDict['dashboard/settings/mongoDB/windGust'] = request.GET['mongoDB_wind_gust']
            formDict['dashboard/settings/mongoDB/rainfall'] = request.GET['mongoDB_rainfall']
            formDict['dashboard/settings/mongoDB/humidity'] = request.GET['mongoDB_humidity']
            formDict['dashboard/settings/mongoDB/pressure'] = request.GET['mongoDB_pressure']
            formDict['dashboard/settings/mongoDB/ambientTemp'] = request.GET['mongoDB_ambient_temp']
            formDict['dashboard/settings/mongoDB/groundTemp'] = request.GET['mongoDB_ground_temp']

            formDict['dashboard/quickLook/periods/windDirection'] = request.GET['quickLook_wind_direction']
            formDict['dashboard/quickLook/periods/avgWindSpeed'] = request.GET['quickLook_avg_wind_speed']
            formDict['dashboard/quickLook/periods/windGust'] = request.GET['quickLook_wind_gust']
            formDict['dashboard/quickLook/periods/rainfall'] = request.GET['quickLook_rainfall']
            formDict['dashboard/quickLook/periods/humidity'] = request.GET['quickLook_humidity']
            formDict['dashboard/quickLook/periods/pressure'] = request.GET['quickLook_pressure']
            formDict['dashboard/quickLook/periods/ambientTemp'] = request.GET['quickLook_ambient_temp']
            formDict['dashboard/quickLook/periods/groundTemp'] = request.GET['quickLook_ground_temp']

            formDict['dashboard/sensors/windDirection'] = request.GET.get('sensors_wind_direction', '')
            formDict['dashboard/sensors/windSpeed'] = request.GET.get('sensors_wind_speed', '')
            formDict['dashboard/sensors/rainfall'] = request.GET.get('sensors_rainfall', '')
            formDict['dashboard/sensors/humidity'] = request.GET.get('sensors_humidity', '')
            formDict['dashboard/sensors/pressure'] = request.GET.get('sensors_pressure', '')
            formDict['dashboard/sensors/ambientTemp'] = request.GET.get('sensors_ambient_temp', '')
            formDict['dashboard/sensors/groundTemp'] = request.GET.get('sensors_ground_temp', '')

            formDict['dashboard/quickLook/format/windDirection'] = request.GET['wind_format']
            formDict['dashboard/settings/SECRET_KEY'] = request.GET['django_secret']

            save_config(formDict)

            return redirect('dashboard')
    else:
        form = ConfigForm()

    context = {'form': form, 'config': get_config()['dashboard']}
    return render(request, 'weatherapp/settings.html', context=context)


admin.site.register_view('settings', view=settings)

# Register your models here.
admin.site.register(Data, DataAdmin)
