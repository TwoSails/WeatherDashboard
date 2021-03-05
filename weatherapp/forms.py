from django import forms

from .models import Data, Config
from .util.config import get_config


class DataForm(forms.ModelForm):
    @staticmethod
    def export(*args, **kwargs):
        print(args, kwargs)

    class Meta:
        model = Data
        fields = ('export_name', 'span_int', 'wind_direction', 'avg_wind_speed', 'wind_gust', 'rainfall', 'humidity',
                  'ambient_temp', 'ground_temp', 'pressure', 'timestamps')


class ConfigForm(forms.ModelForm):
    config = get_config()['dashboard']
    configSettings = config['settings']
    configUnits = configSettings['units']
    configMongo = configSettings['mongoDB']

    tempChoices = [('celsius', 'celsius'), ('fahrenheit', 'fahrenheit')]
    speedChoices = [('km/h', 'km/h'), ('mph', 'mph')]
    rainfallChoices = [('mm', 'mm'), ('inches', 'inches')]
    windChoices = [('txt', 'txt'), ('img', 'img')]

    units_output_temp = forms.ChoiceField(choices=tempChoices)
    units_output_speed = forms.ChoiceField(choices=speedChoices)
    units_output_rainfall = forms.ChoiceField(choices=rainfallChoices)
    units_input_temp = forms.ChoiceField(choices=tempChoices)
    units_input_speed = forms.ChoiceField(choices=speedChoices)
    units_input_rainfall = forms.ChoiceField(choices=rainfallChoices)

    mongoDB_string = forms.CharField(max_length=250, empty_value=configSettings['mongoDBString'], required=False)
    mongoDB_wind_direction = forms.CharField(max_length=100, empty_value=configMongo['windDirection'], required=False)
    mongoDB_recent_speed = forms.CharField(max_length=100, empty_value=configMongo['recentSpeed'], required=False)
    mongoDB_avg_wind_speed = forms.CharField(max_length=100, empty_value=configMongo['avgWindSpeed'], required=False)
    mongoDB_wind_gust = forms.CharField(max_length=100, empty_value=configMongo['windGust'], required=False)
    mongoDB_rainfall = forms.CharField(max_length=100, empty_value=configMongo['rainfall'], required=False)
    mongoDB_humidity = forms.CharField(max_length=100, empty_value=configMongo['humidity'], required=False)
    mongoDB_pressure = forms.CharField(max_length=100, empty_value=configMongo['pressure'], required=False)
    mongoDB_ambient_temp = forms.CharField(max_length=100, empty_value=configMongo['ambientTemp'], required=False)
    mongoDB_ground_temp = forms.CharField(max_length=100, empty_value=configMongo['groundTemp'], required=False)

    quickLook_wind_direction = forms.IntegerField(min_value=30, required=False)
    quickLook_avg_wind_speed = forms.IntegerField(min_value=30, required=False)
    quickLook_wind_gust = forms.IntegerField(min_value=30, required=False)
    quickLook_rainfall = forms.IntegerField(min_value=30, required=False)
    quickLook_humidity = forms.IntegerField(min_value=30, required=False)
    quickLook_pressure = forms.IntegerField(min_value=30, required=False)
    quickLook_ambient_temp = forms.IntegerField(min_value=30, required=False)
    quickLook_ground_temp = forms.IntegerField(min_value=30, required=False)

    sensors_wind_direction = forms.BooleanField(required=False)
    sensors_wind_speed = forms.BooleanField(required=False)
    sensors_rainfall = forms.BooleanField(required=False)
    sensors_humidity = forms.BooleanField(required=False)
    sensors_pressure = forms.BooleanField(required=False)
    sensors_ambient_temp = forms.BooleanField(required=False)
    sensors_ground_temp = forms.BooleanField(required=False)

    django_secret = forms.CharField(max_length=250, required=False)
    wind_format = forms.ChoiceField(choices=windChoices)

    class Meta:
        model = Config
        fields = (
            'django_secret', 'units_output_temp', 'units_output_speed', 'units_output_rainfall', 'units_input_temp',
            'units_input_speed', 'units_input_rainfall', 'mongoDB_string', 'mongoDB_wind_direction',
            'mongoDB_recent_speed',
            'mongoDB_avg_wind_speed', 'mongoDB_wind_gust', 'mongoDB_rainfall', 'mongoDB_humidity', 'mongoDB_pressure',
            'mongoDB_ambient_temp', 'mongoDB_ground_temp')
