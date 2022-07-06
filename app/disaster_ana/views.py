from dataclasses import dataclass
from datetime import date
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db.models import Avg, Count, Sum
from requests import Response
from app.disaster_ana.models import disaster
from django.db.models import F

import json
import pandas as pd
import numpy as np

#########################################################################################################################################################
######################################################### Disaster Modul ################################################################################
#########################################################################################################################################################

# Main Disaster Module view page
def disaster_ana(request):
    # Retrieve data from template
    disaster_selected = request.POST.get('dis_selected')
    impact_selected = request.POST.get('impact_selected')
    level_selected = request.POST.get('level_selected')

    dis_event = disaster.objects.values('event').annotate(count=Count('event')).filter(province_id__startswith='KHM')

    # Set default value
    if impact_selected == None or disaster_selected == None or level_selected == None:
        impact_selected = 'deaths'
        disaster_selected = 'DROUGHT'
        level_selected = 'province_name'
    else:
        impact_selected = impact_selected
        disaster_selected = disaster_selected
        level_selected = level_selected
    
    # Summation data for HighCharts Map
    dis_sum = disaster.objects.values('event', level_selected).annotate(value=Sum(impact_selected)).filter(event=disaster_selected)
    ## Change column name
    dis_sum = dis_sum.values('value').annotate(code=F(level_selected))
    dis_sum = dis_sum.all().filter(code__isnull = False)
    ## Separate as list
    code = list(dis_sum.values_list('code', flat=True))
    value = list(dis_sum.values_list('value', flat=True))
    ## combine 2 list for highchart map
    map_sum = [list(e) for e in zip(code,value)]
    map_sum = json.dumps(map_sum)

    ## Extract year from date column ##
    dis_year = disaster.objects.extra(select={'year': "strftime('%Y',date(date_data))"}).values('year', 'event', 'deaths', 'injured', 'missing', 'house_destroy', 'house_damage')
    df = pd.DataFrame(dis_year)
    df = df.groupby(['year','event']).sum().reset_index()
    df = df.loc[df['event']==disaster_selected]

    list_year = df['year'].to_list()
    list_impact = df[impact_selected].tolist()

    return render(request, "disaster_ana.html", {'url_name': 'disaster_ana', 'event':df  ,'disaster_param':disaster_selected, 
    'impact_param': impact_selected, 'level_param': level_selected, 'dis_event':dis_event,  
    'map_data':map_sum, 'level_code':code, 'level_value':value, 'list_year':list_year, 'list_impact':list_impact})

#########################################################################################################################################################
######################################################### Vulnerability Modul ###########################################################################
#########################################################################################################################################################
def valnerability(request):
    return render(request, "valnerability.html", {'url_name': 'valnerability'})

#########################################################################################################################################################
######################################################### Hazard Modul ##################################################################################
#########################################################################################################################################################
    
# Main hazard Module view page
def hazard_ana(request):
    # Sending disaster type value
    khm_haz_event = disaster.objects.values('event').annotate(count=Count('event')).filter(province_id__startswith='KHM')
    lao_haz_event = disaster.objects.values('event').annotate(count=Count('event')).filter(province_id__startswith='LAO')

    return render(request, "hazard_ana.html", {'url_name': 'hazard_ana', 'khm_haz_event':khm_haz_event, 'lao_haz_event':lao_haz_event})
    
# For 1st submissiom (Load button) in cambodia hazard module
def hazard_cambodia(request): 
    haz = request.POST['khm_haz']
    lev = request.POST['khm_lev']
    ## Create Hazard DataFrame for Cambodia ##
    khm_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(province_id__startswith='KHM'))
    # Add year 
    khm_hazard_df['year'] = pd.DatetimeIndex(khm_hazard_df['date_data']).year
    # Filter by hazard selection
    khm_hazard_df = khm_hazard_df[khm_hazard_df['event']==haz]
    # Get max-Min Year
    year_start = int(khm_hazard_df['year'].min())
    year_end = int(khm_hazard_df['year'].max())
    # Group data for selected level by using function
    khm_data = level_select(lev, khm_hazard_df, year_start,year_end)

    return JsonResponse({'haz': haz, 'lev':lev, 'year_start':year_start, 'year_end':year_end, 'map_data':khm_data}, status=200)
    
# For 2nd submissiom (year range select) in cambodia hzard module
def hazard_cambodia_yearselected(request):
    # Retrieve year
    year_start = int(request.POST['khm_year_start'])
    year_end = int(request.POST['khm_year_end'])
    # Retrieve hazard and level)
    year_haz = request.POST['khm_haz_y']
    year_lev = request.POST['khm_lev_y']

    ## Create Hazard DataFrame for Cambodia ##
    khm_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(province_id__startswith='KHM'))
    # Add year 
    khm_hazard_df['year'] = pd.DatetimeIndex(khm_hazard_df['date_data']).year
    # Filter by hazard selection
    khm_hazard_df = khm_hazard_df[khm_hazard_df['event']==year_haz]
    # Group data for selected level by using function
    khm_data = level_select(year_lev, khm_hazard_df, year_start,year_end)

    return JsonResponse({'end':year_end, 'start':year_start, 'haz':year_haz, 'lev':year_lev, 'map_data':khm_data}, status=200)


### Hazard module : Laos ###

# For 1st submissiom (Load button) in Laos hazard module
def hazard_laos(request): 
    haz = request.POST['lao_haz']
    lev = request.POST['lao_lev']
    ## Create Hazard DataFrame for Cambodia ##
    lao_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(province_id__startswith='LAO'))
    # Add year 
    lao_hazard_df['year'] = pd.DatetimeIndex(lao_hazard_df['date_data']).year
    # Filter by hazard selection
    lao_hazard_df = lao_hazard_df[lao_hazard_df['event']==haz]
    # Get max-Min Year
    year_start = int(lao_hazard_df['year'].min())
    year_end = int(lao_hazard_df['year'].max())
    # Group data for selected level by using function
    lao_data = level_select(lev, lao_hazard_df, year_start,year_end)

    return JsonResponse({'haz': haz, 'lev':lev, 'year_start':year_start, 'year_end':year_end, 'map_data':lao_data}, status=200)
    
# For 2nd submissiom (year range select) in cambodia hzard module
def hazard_laos_yearselected(request):
    # Retrieve year
    year_start = int(request.POST['lao_year_start'])
    year_end = int(request.POST['lao_year_end'])
    # Retrieve hazard and level)
    year_haz = request.POST['lao_haz_y']
    year_lev = request.POST['lao_lev_y']

    ## Create Hazard DataFrame for Cambodia ##
    lao_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(province_id__startswith='LAO'))
    # Add year 
    lao_hazard_df['year'] = pd.DatetimeIndex(lao_hazard_df['date_data']).year
    # Filter by hazard selection
    lao_hazard_df = lao_hazard_df[lao_hazard_df['event']==year_haz]
    # Group data for selected level by using function
    lao_data = level_select(year_lev, lao_hazard_df, year_start,year_end)

    return JsonResponse({'end':year_end, 'start':year_start, 'haz':year_haz, 'lev':year_lev, 'map_data':lao_data}, status=200)

# Create function to prepare the output data groupby level.
def level_select(level, data, year_start,year_end):
    if level == 'commune_name':
        df = data.groupby(['commune_name','year']).count().reset_index()
        df = df.loc[(df['year'] >=year_start) & (df['year'] <= year_end)]
        df = df.groupby(['commune_name']).sum().reset_index()
        code, value = df['commune_name'].to_list(), df['commune_id'].to_list()
        disdata = [list(x) for x in zip(code,value)]
    if level == 'district_name':
        df = data.groupby(['district_name','year']).count().reset_index()
        df = df.loc[(df['year'] >=year_start) & (df['year'] <= year_end)]
        df = df.groupby(['district_name']).sum().reset_index()
        code, value = df['district_name'].to_list(), df['district_id'].to_list()
        disdata = [list(y) for y in zip(code,value)]
    if level == 'province_name':
        df = data.groupby(['province_name','year']).count().reset_index()
        df = df.loc[(df['year'] >=year_start) & (df['year'] <= year_end)]
        df = df.groupby(['province_name']).sum().reset_index()
        code, value = df['province_name'].to_list(), df['province_id'].to_list()
        disdata = [list(z) for z in zip(code,value)]
    return disdata