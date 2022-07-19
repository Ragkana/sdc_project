from django.db import models
from pandas import notnull
from django.db.models import Avg, Count, Min, Sum

# Create your models here.
# Retrieve data from weather_forecast table
class weather_forecast_cambodia(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    date_data = models.DateField()
    province_name = models.CharField(max_length=128, null=False)
    rainfall = models.DecimalField(max_digits=10, decimal_places=2)
    humidity = models.DecimalField(max_digits=10, decimal_places=2)
    max_temp = models.DecimalField(max_digits=10, decimal_places=2)
    min_temp = models.DecimalField(max_digits=10, decimal_places=2)
    windspeed = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = "weather_forecast_cambodia"

class weather_forecast_laos(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    date_data = models.DateField()
    province_name = models.CharField(max_length=128, null=False)
    rainfall = models.DecimalField(max_digits=10, decimal_places=2)
    humidity = models.DecimalField(max_digits=10, decimal_places=2)
    max_temp = models.DecimalField(max_digits=10, decimal_places=2)
    min_temp = models.DecimalField(max_digits=10, decimal_places=2)
    windspeed = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = "weather_forecast_laos"

# Retrieve data from observation_metdata table
class observation_metdata(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    country_id = models.CharField(max_length=10, null=False, db_column='country_id')
    station_name = models.CharField(max_length=128, null=False)
    date_data = models.DateField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    rainfall = models.DecimalField(max_digits=10, decimal_places=2)
    max_t = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    min_t = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    class Meta:
        db_table = "observation_metdata"