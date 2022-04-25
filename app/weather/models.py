from re import T
from django.db import models
from pandas import notnull
from django.db.models import Avg, Count, Min, Sum

# Create your models here.
# Retrieve data from weather_forecast table
class weather_forecast(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    date_data = models.DateField()
    province_name = models.ForeignKey('province', on_delete=models.CASCADE, db_column='province_name', null=False)
    rainfall = models.DecimalField(max_digits=10, decimal_places=2)
    humidity = models.DecimalField(max_digits=10, decimal_places=2)
    max_temp = models.DecimalField(max_digits=10, decimal_places=2)
    min_temp = models.DecimalField(max_digits=10, decimal_places=2)
    windspeed = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = "weather_forecast"
# Retrieve data from observation_metdata table
class observation_metdata(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    country_id = models.ForeignKey('country', on_delete=models.CASCADE, db_column='country_id')
    station_name = models.CharField(max_length=128, null=False)
    date_data = models.DateField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    rainfall = models.DecimalField(max_digits=10, decimal_places=2)
    max_T = models.DecimalField(max_digits=10, decimal_places=2)
    min_T = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        db_table = "observation_metdata"

# Retrieve data from country table
class country(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    country_id = models.CharField(max_length=10, null=False, db_column='country_id')
    country_name = models.CharField(max_length=10, null=False)
    class Meta:
        db_table = "country"

# Retrieve data from province table
class province(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    country_id = models.ForeignKey('country', on_delete=models.CASCADE, db_column='country_id')
    province_id = models.CharField(max_length=10, null=False)
    province_name = models.CharField(max_length=128, null=False)
    class Meta:
        db_table = "province"

# Retrieve data from district table
class district(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    province_id = models.ForeignKey('province', on_delete=models.CASCADE)
    province_name = models.CharField(max_length=128, null=False)
    district_id = models.CharField(max_length=10, null=False)
    district_name = models.CharField(max_length=128, null=False)
    class Meta:
        db_table = "district"

# Retrieve data from ccommune table
class commune(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    district_id = models.ForeignKey('district', on_delete=models.CASCADE)
    district_name = models.CharField(max_length=128, null=False)
    commune_id = models.CharField(max_length=10, null=False)
    commune_name = models.CharField(max_length=10, null=False)
    class Meta:
        db_table = "commune"