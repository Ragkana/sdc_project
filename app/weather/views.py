from datetime import date
import datetime as dt
from itertools import count
from django.shortcuts import render
from django.http import HttpResponse
#from .models import country, observation_metdata, province, district, commune, weather_forecast
from app.weather.models import observation_metdata,weather_forecast
from django.db.models import Avg, Count, Min, Max

import pandas as pd
import numpy as np
import json

# Create your views here.
#def dashboard(request):
    #return HttpResponse("<h2>OMG What's happening</h2>") #Return pure word
#    return render(request, "Dashboard.html", {'url_name': 'dashboard'}) 
    # {'url_name': '......'} put to make it active when click and don't forgrt to add  {% if url_name == 'dashboard' %}active{% endif %} in class where your sidebar link belong.

def login(request):
    return render(request, "login.html")
    
def register(request):
    return render(request, "register.html")

def forgot_password(request):
    return render(request, "forgot-password.html")

def weather_forecast_mod(request):
    # Get input date from template
    date_selected = request.POST.get('selected_date')
    # filter by selected date and retrieve specific column
    wf_date = weather_forecast.objects.filter(date_data=date_selected).values('province_name','rainfall','humidity','max_temp','min_temp','windspeed')
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
    #test = khm_obj['features'][2]['properties']
    khm_obj_json = json.dumps(khm_obj)
    #f_date = weather_forecast.objects.values('date_data').annotate(count=Count('date_data')).order_by('date_data')
    # Get input weather parameter from template
    wf_param_selected = request.POST.get('wf_param')
    return render(request, "weather_fore.html", {'url_name': 'weather_forecast', 'date_pick':date_selected, 'wfparam': wf_param_selected, 'khm_json':khm_obj_json})

def observation(request):
    khm_obj = json.load(open('static/JSON/Cambodia/Cambodia_Province.geojson'))
    # obs : Group station in station name column **use in dropdown**
    obs = observation_metdata.objects.values('station_name').annotate(count=Count('station_name'))
    # Retrieve station name from dropdown
    selected_value = request.POST.get('station_selected')
    ## Set Default Value ##
    if selected_value == None:
        selected_value = 'Battambang'
    else:
        selected_value = selected_value
    ## Average data ##
    # Average data(all year) in selected station and each month, choose only weather data orderby month.
    avg_obs = observation_metdata.objects.values('station_name','month').annotate(rainfall__avg=Avg('rainfall'), max__temp__avg=Avg('max_t'), min__temp__avg=Avg('min_t')).filter(station_name=selected_value).order_by('month')
    rainfall_all = avg_obs.values_list('rainfall__avg', flat=True)
    max_temp_all = avg_obs.values_list('max__temp__avg', flat=True)
    min_temp_all = avg_obs.values_list('min__temp__avg', flat=True)
    ## For Time serie Graph ##
    # Retrieve start and end year
    year_data = observation_metdata.objects.values('station_name').annotate(year__start=Min('year'), year__end=Max('year')).filter(station_name=selected_value)
    year_start, year_end = year_data[0]['year__start'], year_data[0]['year__end']
    #year_start = observation_metdata.objects.values('year', 'station_name').annotate(count=Count('year')).filter(station_name=selected_value).order_by('year')
    #year_end = observation_metdata.objects.values('year', 'station_name').annotate(count=Count('year')).filter(station_name=selected_value).order_by('year')
    # Retrieve year data from template
    start_y_selected = request.POST.get('start_year_selected')
    end_y_selected = request.POST.get('end_year_selected')
    return render(request, "observation.html", {'url_name': 'observation', 'station':obs, 
    'rainfall':rainfall_all, 'max_temp':max_temp_all, 'min_temp':min_temp_all, 'station_n':selected_value, 
    'khm_json':khm_obj, 'year_start':year_start, 'year_end':year_end})

def earthquake(request):
    return render(request, "earthquake.html", {'url_name': 'earthquake'})

def share_data(request):
    return render(request, "share_data.html", {'url_name': 'share_data'})

def sdc_project(request):
    return render(request, "sdc_project.html", {'url_name': 'sdc_project'})

def reports(request):
    return render(request, "reports.html", {'url_name': 'reports'})
