from dataclasses import dataclass
from datetime import date
from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db.models import Avg, Count, Sum
from requests import Response
from app.disaster_ana.models import disaster, vulnerability_mpi
from django.db.models import F

import json
import pandas as pd
import numpy as np

##########################################################################################################################################################
######################################################### Disaster Module ################################################################################
##########################################################################################################################################################

# Main Disaster Module view page
def disaster_ana(request):
    dis_event = disaster.objects.values('event').annotate(count=Count('event')).filter(province_id__startswith='KHM')
    lao_dis_event = disaster.objects.values('event').annotate(count=Count('event')).filter(province_id__startswith='LAO')

    return render(request, "disaster_ana.html", {'url_name': 'disaster_ana', 'dis_event':dis_event, 'lao_dis_event':lao_dis_event})

def disaster_ana_khm(request):
    disaster_selected = request.POST['khm_dis']
    impact_selected = request.POST['khm_impact']
    level_selected = request.POST['khm_level']

    # Summation data for HighCharts Map
    dis_sum = disaster.objects.values('event', level_selected).annotate(value=Sum(impact_selected)).filter(event=disaster_selected).filter(province_id__startswith='KHM')
    ## Change column name
    dis_sum = dis_sum.values('value').annotate(code=F(level_selected))
    dis_sum = dis_sum.all().filter(code__isnull = False)
    ## Separate as list
    code = list(dis_sum.values_list('code', flat=True))
    value = list(dis_sum.values_list('value', flat=True))
    ## combine 2 list for highchart map
    map_sum = [list(e) for e in zip(code,value)]
    #map_sum = json.dumps(map_sum)

    ## Extract year from date column ##
    dis_year = disaster.objects.values('date_data', 'event', 'deaths', 'injured', 'missing', 'house_destroy', 'house_damage').filter(province_id__startswith='KHM')
    # set to dataframe
    df = pd.DataFrame(dis_year)
    # change column type
    df['date_data']= pd.to_datetime(df['date_data'])
    # extract year from date as new column
    df['year'] = pd.DatetimeIndex(df['date_data']).year

    df = df.groupby(['year','event']).sum().reset_index()
    df = df.loc[df['event']==disaster_selected]
    
    list_year = df['year'].to_list()
    list_impact = df[impact_selected].tolist()

    # start and end for Year
    year_start, year_end = min(list_year), max(list_year)

    return JsonResponse({'dis':disaster_selected, 'impact':impact_selected, 'level':level_selected, 'map_data':map_sum, 'level_code':code, 'level_value':value, 'list_year':list_year, 'list_impact':list_impact,
    'year_start':year_start, 'year_end':year_end}, status=200)

def disaster_ana_khm_yearsel(request):
    disaster_selected = request.POST['khm_dis']
    impact_selected = request.POST['khm_impact']
    level_selected = request.POST['khm_level']

    y_start = int(request.POST['khm_year_start'])
    y_end = int(request.POST['khm_year_end'])

    ## Extract year from date column ##
    dis_year = disaster.objects.values('date_data', 'event', 'deaths', 'injured', 'missing', 'house_destroy', 'house_damage', level_selected).filter(province_id__startswith='KHM')
    # set to dataframe
    df = pd.DataFrame(dis_year)
    # change column type
    df['date_data']= pd.to_datetime(df['date_data'])
    # extract year from date as new column
    df['year'] = pd.DatetimeIndex(df['date_data']).year
    df1 = df.loc[(df['year'] >=y_start) & (df['year'] <= y_end) & (df['event'] == disaster_selected)]
    df1 = df1.groupby([level_selected]).sum().reset_index()
    code = df1[level_selected].to_list()
    value = df1[impact_selected].to_list()
    ## combine 2 list for highchart map
    map_sum = [list(e) for e in zip(code,value)]

    return JsonResponse({'dis':disaster_selected, 'impact':impact_selected, 'level':level_selected, 'year_start':y_start, 'year_end':y_end,
    'map_data':map_sum, 'level_code':code, 'level_value':value}, status=200)

    ########## LAOS ##########
def disaster_ana_lao(request):
    disaster_selected = request.POST['lao_dis']
    impact_selected = request.POST['lao_impact']
    level_selected = request.POST['lao_level']

    # Summation data for HighCharts Map
    dis_sum = disaster.objects.values('event', level_selected).annotate(value=Sum(impact_selected)).filter(event=disaster_selected).filter(province_id__startswith='LAO')
    ## Change column name
    dis_sum = dis_sum.values('value').annotate(code=F(level_selected))
    dis_sum = dis_sum.all().filter(code__isnull = False)
    ## Separate as list
    code = list(dis_sum.values_list('code', flat=True))
    value = list(dis_sum.values_list('value', flat=True))
    ## combine 2 list for highchart map
    map_sum = [list(e) for e in zip(code,value)]
    #map_sum = json.dumps(map_sum)

    ## Extract year from date column ##
    dis_year = disaster.objects.values('date_data', 'event', 'deaths', 'injured', 'missing', 'house_destroy', 'house_damage').filter(province_id__startswith='LAO')
    # set to dataframe
    df = pd.DataFrame(dis_year)
    # change column type
    df['date_data']= pd.to_datetime(df['date_data'])
    # extract year from date as new column
    df['year'] = pd.DatetimeIndex(df['date_data']).year

    df = df.groupby(['year','event']).sum().reset_index()
    df = df.loc[df['event']==disaster_selected]
    
    list_year = df['year'].to_list()
    list_impact = df[impact_selected].tolist()

    # start and end for Year
    year_start, year_end = min(list_year), max(list_year)

    return JsonResponse({'dis':disaster_selected, 'impact':impact_selected, 'level':level_selected, 'map_data':map_sum, 'list_year':list_year, 'list_impact':list_impact,
    'year_start':year_start, 'year_end':year_end, 'level_code':code, 'level_value':value}, status=200)

def disaster_ana_lao_yearsel(request):
    disaster_selected = request.POST['lao_dis']
    impact_selected = request.POST['lao_impact']
    level_selected = request.POST['lao_level']

    y_start = int(request.POST['lao_year_start'])
    y_end = int(request.POST['lao_year_end'])

    ## Extract year from date column ##
    dis_year = disaster.objects.values('date_data', 'event', 'deaths', 'injured', 'missing', 'house_destroy', 'house_damage', level_selected).filter(province_id__startswith='LAO')
    # set to dataframe
    df = pd.DataFrame(dis_year)
    # change column type
    df['date_data']= pd.to_datetime(df['date_data'])
    # extract year from date as new column
    df['year'] = pd.DatetimeIndex(df['date_data']).year
    df1 = df.loc[(df['year'] >=y_start) & (df['year'] <= y_end) & (df['event'] == disaster_selected)]
    df1 = df1.groupby([level_selected]).sum().reset_index()
    code = df1[level_selected].to_list()
    value = df1[impact_selected].to_list()
    ## combine 2 list for highchart map
    map_sum = [list(e) for e in zip(code,value)]

    return JsonResponse({'dis':disaster_selected, 'impact':impact_selected, 'level':level_selected, 'year_start':y_start, 'year_end':y_end,
    'map_data':map_sum, 'level_code':code, 'level_value':value}, status=200)

#########################################################################################################################################################
######################################################### Vulnerability Modul ###########################################################################
#########################################################################################################################################################
def vulnerability(request):
    return render(request, "vulnerability.html", {'url_name': 'vulnerability'})

#### Cambodia ####
def vul_khm_population(request):
    pop_select = request.POST['khm_pop_type']
    pop_data = vulnerability_mpi.objects.values('country_id',pop_select, 'province_name').filter(country_id='KHM')
    value = list(pop_data.values_list(pop_select, flat=True))
    value = listConvertDataType(value)
    area = list(pop_data.values_list('province_name', flat=True))

    popmap_sum = [list(e) for e in zip(area,value)]
    return JsonResponse({'pop_select':pop_select, 'pop_map_data':popmap_sum}, status=200)

def vul_khm_mpi(request):
    mpi_select = request.POST['khm_mpi_type']
    mpi_data = vulnerability_mpi.objects.values('country_id', mpi_select, 'province_name').filter(country_id='KHM')
    value = list(mpi_data.values_list(mpi_select, flat=True))
    value = listConvertDataType(value)
    area = list(mpi_data.values_list('province_name', flat=True))

    mpimap_sum = [list(e) for e in zip(area,value)]
    return JsonResponse({'mpi_select':mpi_select, 'mpi_map_data':mpimap_sum}, status=200)

#### Laos ####
def vul_lao_population(request):
    pop_select = request.POST['lao_pop_type']
    pop_data = vulnerability_mpi.objects.values('country_id',pop_select, 'province_name').filter(country_id='LAO')
    value = list(pop_data.values_list(pop_select, flat=True))
    value = listConvertDataType(value)
    area = list(pop_data.values_list('province_name', flat=True))

    popmap_sum = [list(e) for e in zip(area,value)]
    return JsonResponse({'pop_select':pop_select, 'pop_map_data':popmap_sum}, status=200)

def vul_lao_mpi(request):
    mpi_select = request.POST['lao_mpi_type']
    mpi_data = vulnerability_mpi.objects.values('country_id', mpi_select, 'province_name').filter(country_id='LAO')
    value = list(mpi_data.values_list(mpi_select, flat=True))
    value = listConvertDataType(value)
    area = list(mpi_data.values_list('province_name', flat=True))

    mpimap_sum = [list(e) for e in zip(area,value)]
    return JsonResponse({'mpi_select':mpi_select, 'mpi_map_data':mpimap_sum}, status=200)
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

## Function for converting data in list from string to float
# Using for Observation page to convert string list of weather parameter (rainfall, min temp and max temp) to float.
def listConvertDataType(li):
    for i in range(0, len(li)):
        li[i] = float(li[i])
    return li