from audioop import avg
from itertools import count
from django.shortcuts import render
from django.http import HttpResponse
from .models import country, observation_metdata, province, district, commune
from django.db.models import Avg, Count

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

def weather_forecast(request):
    
    return render(request, "weather_fore.html", {'url_name': 'weather_forecast'})

def observation(request):
    # obs : Group station in station name column **use in dropdown**
    obs = observation_metdata.objects.values('station_name').annotate(count=Count('station_name'))
    # Retrieve station name from dropdown
    selected_value = request.POST.get('station_selected')
    # Average data in selected station and each month, choose only weather data orderby month.
    avg_obs = observation_metdata.objects.values('station_name','month').annotate(rainfall__avg=Avg('rainfall'), max__temp__avg=Avg('max_T'), min__temp__avg=Avg('min_T')).filter(station_name=selected_value).order_by('month')
    rainfall = avg_obs.values_list('rainfall__avg', flat=True)
    max_temp = avg_obs.values_list('max__temp__avg', flat=True)
    min_temp = avg_obs.values_list('min__temp__avg', flat=True)
    return render(request, "observation.html", {'url_name': 'observation', 'station':obs, 'rainfall':rainfall, 'max_temp':max_temp, 'min_temp':min_temp, 'station_n':selected_value})

def hazard_ana(request):
    return render(request, "hazard_ana.html", {'url_name': 'hazard_ana'})

def disaster_ana(request):
    return render(request, "disaster_ana.html", {'url_name': 'disaster_ana'})

def earthquake(request):
    return render(request, "earthquake.html", {'url_name': 'earthquake'})

def share_data(request):
    return render(request, "share_data.html", {'url_name': 'share_data'})

def sdc_project(request):
    return render(request, "sdc_project.html", {'url_name': 'sdc_project'})

def reports(request):
    return render(request, "reports.html", {'url_name': 'reports'})
