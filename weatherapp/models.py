from django.db import models
from django.utils import timezone


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'


class Data(models.Model):
    name = f'{str(timezone.now()).replace(" ", "_")}_export.json'
    export_name = models.CharField(max_length=int(len(name) + 5), default=name)
    span_int = models.IntegerField(name="span_int", default=7)
    wind_direction = models.BooleanField(name='wind_direction', default=False)
    avg_wind_speed = models.BooleanField(name="avg_wind_speed", default=False)
    wind_gust = models.BooleanField(name="wind_gust", default=False)
    rainfall = models.BooleanField(name="rainfall", default=False)
    humidity = models.BooleanField(name="humidity", default=False)
    ambient_temp = models.BooleanField(name="ambient_temp", default=False)
    ground_temp = models.BooleanField(name="ground_temp", default=False)
    pressure = models.BooleanField(name="pressure", default=False)
    timestamps = models.BooleanField(name="timestamps", default=False)

    def export(self):
        pass

    def __str__(self):
        return self.export_name, self.span_int, self.wind_direction, self.avg_wind_speed, self.wind_gust, self.rainfall, \
               self.humidity, self.ambient_temp, self.ground_temp, self.pressure, self.timestamps


class Config(models.Model):

    def __str__(self):
        pass
