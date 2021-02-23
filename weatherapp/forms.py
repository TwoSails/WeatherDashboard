from django import forms

from .models import Data


class DataForm(forms.ModelForm):
    def export(self, *args):
        print(args)

    class Meta:
        model = Data
        fields = ('export_name', 'span_int', 'wind_direction', 'avg_wind_speed', 'wind_gust', 'rainfall', 'humidity',
                  'ambient_temp', 'ground_temp', 'pressure', 'timestamps')
