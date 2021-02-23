from django.contrib import admin

from .models import Data


class DataAdmin(admin.ModelAdmin):
    list_display = (
        'export_name', 'span_int', 'wind_direction', 'avg_wind_speed', 'wind_gust', 'rainfall', 'humidity',
        'ambient_temp', 'ground_temp', 'pressure', 'timestamps')


# Register your models here.
admin.site.register(Data, DataAdmin)
