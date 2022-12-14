from datetime import date
import datetime as dt
from itertools import count
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# Database
from app.weather.models import observation_metdata,weather_forecast_cambodia,weather_forecast_laos
from app.disaster_ana.models import sdc_project_location_cambodia, sdc_project_location_laos, sdc_project_location_myanmar

from django.db.models import Avg, Count, Min, Max
from django.contrib.auth.decorators import login_required, permission_required

import pandas as pd
import numpy as np
import json

# Create your views here.
#def dashboard(request):
    #return HttpResponse("<h2>OMG What's happening</h2>") #Return pure word
#    return render(request, "Dashboard.html", {'url_name': 'dashboard'}) 
    # {'url_name': '......'} put to make it active when click and don't forgrt to add  {% if url_name == 'dashboard' %}active{% endif %} in class where your sidebar link belong.

@login_required(login_url='login')
def weather_forecast_mod(request):
    # Sending SDC project value
    khm_sdc = sdc_project_location_cambodia.objects.values('project').annotate(count=Count('project'))
    lao_sdc = sdc_project_location_laos.objects.values('project').annotate(count=Count('project'))
    #mya_sdc = sdc_project_location_myanmar.objects.values('project').annotate(count=Count('project'))

    ## Sending SDC project latitude and longitude ##
    # Cambodia
    khm_loc = pd.DataFrame(sdc_project_location_cambodia.objects.values('id', 'project', 'country_id', 'country_name', 'province_id', 'province_name', 'district_id', 'district_name',
    'commune_id', 'commune_name', 'latitude', 'longitude', 'detail'))
    khm_data = project_location_JSON(khm_loc)
        
    # Laos
    lao_loc = pd.DataFrame(sdc_project_location_laos.objects.values('id', 'project', 'country_id', 'country_name', 'province_id', 'province_name', 'district_id', 'district_name',
    'commune_id', 'commune_name', 'latitude', 'longitude', 'detail'))
    lao_data = project_location_JSON(lao_loc)

    # Myanmar
    #mya_loc = pd.DataFrame(sdc_project_location_myanmar.objects.values('id', 'project', 'country_id', 'country_name', 'province_id', 'province_name', 'district_id', 'district_name',
    #'commune_id', 'commune_name', 'latitude', 'longitude', 'detail'))
    #mya_data = project_location_JSON(mya_loc)
    return render(request, "weather_fore.html", {'url_name': 'weather_forecast', 'khm_project':khm_data, 'lao_project':lao_data, 'khm_sdc':khm_sdc, 'lao_sdc':lao_sdc})

# Function for cambodia AJAX in weather forecate module
def wf_cambodia_submit(request):
    khm_date_selected = request.POST['khm_date']
    khm_wf_param = request.POST['khm_wf_param']
    # filter by selected date and retrieve specific column
    wf_date = weather_forecast_cambodia.objects.filter(date_data=khm_date_selected).values('province_name','rainfall','humidity','max_temp','min_temp','windspeed')
    # save query as dataframe
    wf = pd.DataFrame(wf_date)
    # load GeoJSON file here
    khm_obj = json.load(open('static/JSON/Cambodia/Cambodia_Province.geojson'))
    # Combine data
    for index,row in wf.iterrows():
        prov = row['province_name']
        # Append in dict
        for d in khm_obj['features']:
            if d['properties']['Province'] == prov:
                d['properties']['rainfall'] = float(row['rainfall'])
                d['properties']['humidity'] = float(row['humidity'])
                d['properties']['max_temp'] = float(row['max_temp'])
                d['properties']['min_temp'] = float(row['min_temp'])
                d['properties']['windspeed'] = float(row['windspeed'])
            else :
                pass
    #khm_obj = json.dumps(khm_obj)

    return JsonResponse({'date_sel':khm_date_selected, 'wf_param':khm_wf_param, 'khm_map_data':khm_obj}, status=200)

# Function for cambodia AJAX in weather forecate module
def wf_laos_submit(request):
    lao_date_selected = request.POST['lao_date']
    lao_wf_param = request.POST['lao_wf_param']
    # filter by selected date and retrieve specific column
    wf_date = weather_forecast_laos.objects.filter(date_data=lao_date_selected).values('province_name','rainfall','humidity','max_temp','min_temp','windspeed')
    # save query as dataframe
    wf = pd.DataFrame(wf_date)
    # load GeoJSON file here
    laos_obj = json.load(open('static/JSON/Laos/Laos_Province.geojson'))
    # Combine data
    for index,row in wf.iterrows():
        prov = row['province_name']
        # Append in dict
        for d in laos_obj['features']:
            if d['properties']['Province'] == prov:
                d['properties']['rainfall'] = float(row['rainfall'])
                d['properties']['humidity'] = float(row['humidity'])
                d['properties']['max_temp'] = float(row['max_temp'])
                d['properties']['min_temp'] = float(row['min_temp'])
                d['properties']['windspeed'] = float(row['windspeed'])
            else :
                pass
    return JsonResponse({'date_sel':lao_date_selected, 'wf_param':lao_wf_param, 'lao_map_data':laos_obj}, status=200)

#########################################################################################################################################################
################################################################# Observation Module ####################################################################
#########################################################################################################################################################
@login_required(login_url='login')
def observation(request):
    khm_obj = json.load(open('static/JSON/Cambodia/Cambodia_Province.geojson'))
    lao_obj = json.load(open('static/JSON/Laos/Laos_Province.geojson'))
    # obs : Group station in station name column **use in dropdown**
    khm_obs = observation_metdata.objects.values('station_name').annotate(count=Count('station_name')).filter(country_id='KHM')
    lao_obs = observation_metdata.objects.values('station_name').annotate(count=Count('station_name')).filter(country_id='LAO')

    return render(request, "observation.html", {'url_name': 'observation', 'khm_station':khm_obs, 'khm_json':khm_obj, 'lao_station':lao_obs, 'lao_json':lao_obj})

def obs_khm_station(request):
    khm_station = request.POST['khm_station']
    ## Average data ##
    # Average data(all year) in selected station and each month, choose only weather data orderby month.
    avg_obs = observation_metdata.objects.values('station_name','month').annotate(rainfall__avg=Avg('rainfall'), max__temp__avg=Avg('max_t'), min__temp__avg=Avg('min_t')).filter(station_name=khm_station).order_by('month').filter(country_id='KHM')
    rainfall_all = avg_obs.values_list('rainfall__avg', flat=True)
    rainfall_all = list(rainfall_all)
    rainfall_all = listConvertDataType(rainfall_all)
    max_temp_all = avg_obs.values_list('max__temp__avg', flat=True)
    max_temp_all = list(max_temp_all)
    max_temp_all = listConvertDataType(max_temp_all)
    min_temp_all = avg_obs.values_list('min__temp__avg', flat=True)
    min_temp_all = list(min_temp_all)
    min_temp_all = listConvertDataType(min_temp_all)

    ## Year Range ##
    year_data = observation_metdata.objects.values('station_name').annotate(year__start=Min('year'), year__end=Max('year')).filter(station_name=khm_station)
    year_start, year_end = year_data[0]['year__start'], year_data[0]['year__end']
    
    return JsonResponse({'station':khm_station, 'rainfall':rainfall_all, 'max_temp':max_temp_all, 'min_temp':min_temp_all, 'year_start':year_start, 'year_end':year_end}, status=200)

def obs_khm_station_yearsel(request):
    # Retrieve year
    year_start = int(request.POST['khm_year_start'])
    year_end = int(request.POST['khm_year_end'])
    khm_station = request.POST['khm_station_y']

    ## Observation Module : Data output for year selection
    year_obs = observation_metdata.objects.all().values('station_name', 'month').filter(year__range=(year_start, year_end)).annotate(rainfall__avg=Avg('rainfall'), max__temp__avg=Avg('max_t'), min__temp__avg=Avg('min_t')).filter(station_name=khm_station)
    rainfall = list(year_obs.values_list('rainfall__avg', flat=True))
    rainfall = listConvertDataType(rainfall)
    max_t = list(year_obs.values_list('max__temp__avg', flat=True))
    max_t = listConvertDataType(max_t)
    min_t = list(year_obs.values_list('min__temp__avg', flat=True))
    min_t = listConvertDataType(min_t)

    return JsonResponse({'year_start':year_start, 'year_end':year_end, 'rainfall':rainfall, 'max_temp':max_t, 'min_temp':min_t}, status=200)

def obs_lao_station(request):
    lao_station = request.POST['lao_station']
    ## Average data ##
    # Average data(all year) in selected station and each month, choose only weather data orderby month.
    avg_obs = observation_metdata.objects.values('station_name','month').annotate(rainfall__avg=Avg('rainfall'), max__temp__avg=Avg('max_t'), min__temp__avg=Avg('min_t')).filter(station_name=lao_station).order_by('month').filter(country_id='LAO')
    rainfall_all = avg_obs.values_list('rainfall__avg', flat=True)
    rainfall_all = list(rainfall_all)
    rainfall_all = listConvertDataType(rainfall_all)
    max_temp_all = avg_obs.values_list('max__temp__avg', flat=True)
    max_temp_all = list(max_temp_all)
    max_temp_all = listConvertDataType(max_temp_all)
    min_temp_all = avg_obs.values_list('min__temp__avg', flat=True)
    min_temp_all = list(min_temp_all)
    min_temp_all = listConvertDataType(min_temp_all)

    ## Year Range ##
    year_data = observation_metdata.objects.values('station_name').annotate(year__start=Min('year'), year__end=Max('year')).filter(station_name=lao_station)
    year_start, year_end = year_data[0]['year__start'], year_data[0]['year__end']
    
    return JsonResponse({'station':lao_station, 'rainfall':rainfall_all, 'max_temp':max_temp_all, 'min_temp':min_temp_all, 'year_start':year_start, 'year_end':year_end}, status=200)

def obs_lao_station_yearsel(request):
    # Retrieve year
    year_start = int(request.POST['lao_year_start'])
    year_end = int(request.POST['lao_year_end'])
    lao_station = request.POST['lao_station_y']

    ## Observation Module : Data output for year selection
    year_obs = observation_metdata.objects.all().values('station_name', 'month').filter(year__range=(year_start, year_end)).annotate(rainfall__avg=Avg('rainfall'), max__temp__avg=Avg('max_t'), min__temp__avg=Avg('min_t')).filter(station_name=lao_station)
    rainfall = list(year_obs.values_list('rainfall__avg', flat=True))
    rainfall = listConvertDataType(rainfall)
    max_t = list(year_obs.values_list('max__temp__avg', flat=True))
    max_t = listConvertDataType(max_t)
    min_t = list(year_obs.values_list('min__temp__avg', flat=True))
    min_t = listConvertDataType(min_t)

    return JsonResponse({'year_start':year_start, 'year_end':year_end, 'rainfall':rainfall, 'max_temp':max_t, 'min_temp':min_t}, status=200)



## Function for converting data in list from string to float
# Using for Observation page to convert string list of weather parameter (rainfall, min temp and max temp) to float.
def listConvertDataType(li):
    for i in range(0, len(li)):
        li[i] = float(li[i])
    return li




def earthquake(request):
    return render(request, "earthquake.html", {'url_name': 'earthquake'})

#### For Location data display ####
def project_location_JSON(df):
    project = df['project'].to_list() 
    index = df['id'].to_list()
    lat, long = df['latitude'].to_list(), df['longitude'].to_list()
    # Convert data type from decimal to float
    lat, long = np.array(lat, float), np.array(long, float)
    location = [list(x) for x in zip(lat,long)]
    dict_data = {}
    for a, b, c in zip(index, project, location):
        dict_data[a] = dict(Project=b, location=c)
    json_data = json.dumps(dict_data)
    return json_data
