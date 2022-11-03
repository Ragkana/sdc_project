# Import database for this application
from lib2to3.pgen2 import driver
from turtle import title
from urllib import response
from app.disaster_ana.models import disaster, vulnerability_mpi, sdc_project_location_cambodia, sdc_project_location_laos

from django.shortcuts import render
from django.http import JsonResponse,HttpResponse, FileResponse
from django.db.models import Avg, Count, Sum
from requests import Response
from django.db.models import F
from django.contrib.auth.decorators import login_required, permission_required

# Python Library for CSV file download
import csv
from django.utils.encoding import smart_str

# Python Library for python dataframe
import json
import pandas as pd
import numpy as np

##########################################################################################################################################################
######################################################### Disaster Module ################################################################################
##########################################################################################################################################################

# Main Disaster Module view page
@login_required(login_url='login')
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
## Vulnerability Main page ##
@login_required(login_url='login')
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

##########################################################################################################################################################
######################################################### Hazard Module ##################################################################################
##########################################################################################################################################################
    
# Main hazard Module view page
@login_required(login_url='login')
def hazard_ana(request):
    # Sending disaster type value
    khm_haz_event = disaster.objects.values('event').annotate(count=Count('event')).filter(province_id__startswith='KHM')
    lao_haz_event = disaster.objects.values('event').annotate(count=Count('event')).filter(province_id__startswith='LAO')

    # Sending SDC project value
    khm_sdc = sdc_project_location_cambodia.objects.values('project').annotate(count=Count('project'))
    lao_sdc = sdc_project_location_laos.objects.values('project').annotate(count=Count('project'))

    ## Sending SDC project latitude and longitude ##
    # Cambodia
    khm_loc = pd.DataFrame(sdc_project_location_cambodia.objects.values('id', 'project', 'country_id', 'country_name', 'province_id', 'province_name', 'district_id', 'district_name',
    'commune_id', 'commune_name', 'latitude', 'longitude', 'detail'))
    khm_data = project_location_JSON(khm_loc)
        
    # Laos
    lao_loc = pd.DataFrame(sdc_project_location_laos.objects.values('id', 'project', 'country_id', 'country_name', 'province_id', 'province_name', 'district_id', 'district_name',
    'commune_id', 'commune_name', 'latitude', 'longitude', 'detail'))
    lao_data = project_location_JSON(lao_loc)

    return render(request, "hazard_ana_edit.html", {'url_name': 'hazard_ana', 'khm_haz_event':khm_haz_event, 'lao_haz_event':lao_haz_event, 
    'khm_project':khm_data, 'lao_project':lao_data, 'khm_sdc':khm_sdc, 'lao_sdc':lao_sdc})

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
    
# For 1st submissiom (Load button) in cambodia hazard module
def hazard_cambodia(request): 
    haz = request.POST['khm_haz']
    lev = request.POST['khm_lev']
    ## Create Hazard DataFrame for Cambodia ##
    if lev == 'province_name' :
        khm_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(province_id__startswith='KHM'))
    if lev == 'district_name':
        khm_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(district_id__startswith='KHM'))
    if lev == 'commune_name':
        khm_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(commune_id__startswith='KHM'))
    # Add year 
    khm_hazard_df['year'] = pd.DatetimeIndex(khm_hazard_df['date_data']).year
    # Filter by hazard selection
    khm_hazard_df = khm_hazard_df[khm_hazard_df['event']==haz]
    # Get max-Min Year
    year_start = int(khm_hazard_df['year'].min())
    year_end = int(khm_hazard_df['year'].max())
    # import GEOJSON file
    khm_province, khm_province2 = json.load(open('static/JSON/Cambodia/Cambodia_Province.geojson')), json.load(open('static/JSON/Cambodia/Cambodia_Province.geojson'))
    khm_district, khm_district2 = json.load(open('static/JSON/Cambodia/Cambodia_District.geojson')), json.load(open('static/JSON/Cambodia/Cambodia_District.geojson'))
    khm_commune, khm_commune2 = json.load(open('static/JSON/Cambodia/Cambodia_Commune.geojson')), json.load(open('static/JSON/Cambodia/Cambodia_Commune.geojson'))
    # Group data for selected level by using function
    khm_data = level_select(lev, khm_hazard_df, year_start, year_end, province = khm_province, district = khm_district, commune = khm_commune)
    khm_data_out = to_GeoJSON_download(lev, khm_hazard_df, year_start, year_end, province = khm_province2, district = khm_district2, commune = khm_commune2)

    return JsonResponse({'haz': haz, 'lev':lev, 'year_start':year_start, 'year_end':year_end, 'map_data':khm_data, 'mapdata_out':khm_data_out}, status=200)
    
# For 2nd submissiom (year range select) in cambodia hzard module
def hazard_cambodia_yearselected(request):
    # Retrieve year
    year_start = int(request.POST['khm_year_start'])
    year_end = int(request.POST['khm_year_end'])
    # Retrieve hazard and level)
    year_haz = request.POST['khm_haz_y']
    year_lev = request.POST['khm_lev_y']

    ## Create Hazard DataFrame for Cambodia ##
    if year_lev == 'province_name' :
        khm_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(province_id__startswith='KHM'))
    if year_lev == 'district_name':
        khm_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(district_id__startswith='KHM'))
    if year_lev == 'commune_name':
        khm_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(commune_id__startswith='KHM'))
    # Add year 
    khm_hazard_df['year'] = pd.DatetimeIndex(khm_hazard_df['date_data']).year
    # Filter by hazard selection
    khm_hazard_df = khm_hazard_df[khm_hazard_df['event']==year_haz]
    # import GEOJSON file
    khm_province, khm_province2 = json.load(open('static/JSON/Cambodia/Cambodia_Province.geojson')), json.load(open('static/JSON/Cambodia/Cambodia_Province.geojson'))
    khm_district, khm_district2 = json.load(open('static/JSON/Cambodia/Cambodia_District.geojson')), json.load(open('static/JSON/Cambodia/Cambodia_District.geojson'))
    khm_commune, khm_commune2 = json.load(open('static/JSON/Cambodia/Cambodia_Commune.geojson')), json.load(open('static/JSON/Cambodia/Cambodia_Commune.geojson'))
    # Group data for selected level by using function
    khm_data = level_select(year_lev, khm_hazard_df, year_start,year_end, province = khm_province, district = khm_district, commune = khm_commune)
    khm_data_out = to_GeoJSON_download(year_lev, khm_hazard_df, year_start,year_end, province = khm_province2, district = khm_district2, commune = khm_commune2)

    return JsonResponse({'end':year_end, 'start':year_start, 'haz':year_haz, 'lev':year_lev, 'map_data':khm_data, 'mapdata_out':khm_data_out}, status=200)

# For Cambodia csv file download
def hazard_khm_csv(request):
	# response content type
	response = HttpResponse(content_type='text/csv')
	#decide the file name
	response['Content-Disposition'] = 'attachment; filename="cambodia_disdata.csv"'

	writer = csv.writer(response, csv.excel)
	response.write(u'\ufeff'.encode('utf8'))

	#write the headers
	writer.writerow([
		smart_str(u"province_id"),
		smart_str(u"province_name"),
		smart_str(u"district_id"),
        smart_str(u"district_name"),
        smart_str(u"commune_id"),
        smart_str(u"commune_name"),
        smart_str(u"date"),
        smart_str(u"event"),
        #smart_str(u"datacard_records"),
        smart_str(u"deaths"),
        smart_str(u"injured"),
        smart_str(u"missing"),
        smart_str(u"house_destroy"),
        smart_str(u"house_damage")
	])
	#get data from database or from text file....
	data = disaster.objects.values_list('province_id','province_name','district_id','district_name','commune_id','commune_name','date_data','event','deaths','injured','missing',
    'house_destroy','house_damage').filter(province_id__startswith='KHM')
	for a in data:
		writer.writerow(a)

	return response


### Hazard module : Laos ###

# For 1st submissiom (Load button) in Laos hazard module
def hazard_laos(request): 
    haz = request.POST['lao_haz']
    lev = request.POST['lao_lev']
    ## Create Hazard DataFrame for Laos ##
    if lev == 'province_name' :
        lao_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(province_id__startswith='LAO'))
    if lev == 'district_name':
        lao_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(district_id__startswith='LAO'))
    # Add year 
    lao_hazard_df['year'] = pd.DatetimeIndex(lao_hazard_df['date_data']).year
    # Filter by hazard selection
    lao_hazard_df = lao_hazard_df[lao_hazard_df['event']==haz]
    # Get max-Min Year
    year_start = int(lao_hazard_df['year'].min())
    year_end = int(lao_hazard_df['year'].max())
    # import GEOJSON file
    lao_province, lao_province2 = json.load(open('static/JSON/Laos/Laos_Province.geojson')), json.load(open('static/JSON/Laos/Laos_Province.geojson'))
    lao_district, lao_district2 = json.load(open('static/JSON/Laos/Laos_District.geojson')), json.load(open('static/JSON/Laos/Laos_District.geojson'))
    # Group data for selected level by using function
    lao_data = level_select(lev, lao_hazard_df, year_start, year_end, province = lao_province, district = lao_district, commune=None)
    lao_data_out = to_GeoJSON_download(lev, lao_hazard_df, year_start, year_end, province = lao_province2, district = lao_district2, commune=None)

    return JsonResponse({'haz': haz, 'lev':lev, 'year_start':year_start, 'year_end':year_end, 'map_data':lao_data, 'mapdata_out':lao_data_out}, status=200)
    
# For 2nd submissiom (year range select) in cambodia hzard module
def hazard_laos_yearselected(request):
    # Retrieve year
    year_start = int(request.POST['lao_year_start'])
    year_end = int(request.POST['lao_year_end'])
    # Retrieve hazard and level)
    year_haz = request.POST['lao_haz_y']
    year_lev = request.POST['lao_lev_y']

    ## Create Hazard DataFrame for Laos ##
    if year_lev == 'province_name' :
        lao_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(province_id__startswith='LAO'))
    if year_lev == 'district_name':
        lao_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(district_id__startswith='LAO'))
    # Add year 
    lao_hazard_df['year'] = pd.DatetimeIndex(lao_hazard_df['date_data']).year
    # Filter by hazard selection
    lao_hazard_df = lao_hazard_df[lao_hazard_df['event']==year_haz]
    # import GEOJSON file
    lao_province, lao_province2 = json.load(open('static/JSON/Laos/Laos_Province.geojson')), json.load(open('static/JSON/Laos/Laos_Province.geojson'))
    lao_district, lao_district2 = json.load(open('static/JSON/Laos/Laos_District.geojson')), json.load(open('static/JSON/Laos/Laos_District.geojson'))
    # Group data for selected level by using function
    lao_data = level_select(year_lev, lao_hazard_df, year_start, year_end, province = lao_province, district = lao_district, commune=None)
    lao_data_out = to_GeoJSON_download(year_lev, lao_hazard_df, year_start, year_end, province = lao_province2, district = lao_district2, commune=None)

    return JsonResponse({'end':year_end, 'start':year_start, 'haz':year_haz, 'lev':year_lev, 'map_data':lao_data, 'mapdata_out':lao_data_out}, status=200)

# For Laos csv file download
def hazard_lao_csv(request):
	# response content type
	response = HttpResponse(content_type='text/csv')
	#decide the file name
	response['Content-Disposition'] = 'attachment; filename="laos_disdata.csv"'

	writer = csv.writer(response, csv.excel)
	response.write(u'\ufeff'.encode('utf8'))

	#write the headers
	writer.writerow([
		smart_str(u"province_id"),
		smart_str(u"province_name"),
		smart_str(u"district_id"),
        smart_str(u"district_name"),
        smart_str(u"commune_id"),
        smart_str(u"commune_name"),
        smart_str(u"date"),
        smart_str(u"event"),
        #smart_str(u"datacard_records"),
        smart_str(u"deaths"),
        smart_str(u"injured"),
        smart_str(u"missing"),
        smart_str(u"house_destroy"),
        smart_str(u"house_damage")
	])
	#get data from database or from text file....
	data = disaster.objects.values_list('province_id','province_name','district_id','district_name','commune_id','commune_name','date_data','event','deaths','injured','missing',
    'house_destroy','house_damage').filter(province_id__startswith='LAO')
	for b in data:
		writer.writerow(b)

	return response

## ---------------------------------------------------------------------------------------------------------------------- ##

# Create function to prepare the output data groupby level.
def level_select(level, data, year_start,year_end, province, district, commune):
    if level == 'commune_name':
        df = data.groupby(['commune_name','year']).count().reset_index()
        df = df.loc[(df['year'] >=year_start) & (df['year'] <= year_end)]
        df = df.groupby(['commune_name']).sum().reset_index()
        # Add percentage column
        df['percentage'] = (df.commune_id / df.commune_id.max()) * 100
        for index,row in df.iterrows():
            comm = row['commune_name']
            # Append in dict
            for c in commune['features']:
                if c['properties']['Commune'] == comm:
                    c['properties']['value'] = float(row['commune_id'])
                    c['properties']['percentage'] = float(row['percentage'])
        disdata = commune
    if level == 'district_name':
        df = data.groupby(['district_name','year']).count().reset_index()
        df = df.loc[(df['year'] >=year_start) & (df['year'] <= year_end)]
        df = df.groupby(['district_name']).sum().reset_index()
        # Add percentage column
        df['percentage'] = (df.district_id / df.district_id.max()) * 100
        for index,row in df.iterrows():
            dist = row['district_name']
            # Append in dict
            for d in district['features']:
                if d['properties']['District'] == dist:
                    d['properties']['value'] = float(row['district_id'])
                    d['properties']['percentage'] = float(row['percentage'])
        disdata = district
    if level == 'province_name':
        df = data.groupby(['province_name','year']).count().reset_index()
        df = df.loc[(df['year'] >=year_start) & (df['year'] <= year_end)]
        df = df.groupby(['province_name']).sum().reset_index()
        # Add percentage column
        df['percentage'] = (df.province_id / df.province_id.max()) * 100
        for index,row in df.iterrows():
            prov = row['province_name']
            # Append in dict
            for p in province['features']:
                if p['properties']['Province'] == prov:
                    p['properties']['value'] = float(row['province_id'])
                    p['properties']['percentage'] = float(row['percentage'])
        disdata = province
    return disdata

# Create function for download GeoJSON file (remove percentage)
def to_GeoJSON_download(level, data, year_start,year_end, province, district, commune):
    if level == 'commune_name':
        df2 = data.groupby(['commune_name','year']).count().reset_index()
        df2 = df2.loc[(df2['year'] >=year_start) & (df2['year'] <= year_end)]
        df2 = df2.groupby(['commune_name']).sum().reset_index()
        for index,row in df2.iterrows():
            comm2 = row['commune_name']
            # Append in dict
            for cc in commune['features']:
                if cc['properties']['Commune'] == comm2:
                    cc['properties']['freq'] = float(row['commune_id'])
        disdata_out = commune
    if level == 'district_name':
        df2 = data.groupby(['district_name','year']).count().reset_index()
        df2 = df2.loc[(df2['year'] >=year_start) & (df2['year'] <= year_end)]
        df2 = df2.groupby(['district_name']).sum().reset_index()
        for index,row in df2.iterrows():
            dist2 = row['district_name']
            # Append in dict
            for dd in district['features']:
                if dd['properties']['District'] == dist2:
                    dd['properties']['freq'] = float(row['district_id'])
        disdata_out = district
    if level == 'province_name':
        df2 = data.groupby(['province_name','year']).count().reset_index()
        df2 = df2.loc[(df2['year'] >=year_start) & (df2['year'] <= year_end)]
        df2 = df2.groupby(['province_name']).sum().reset_index()
        for index,row in df2.iterrows():
            prov2 = row['province_name']
            # Append in dict
            for pp in province['features']:
                if pp['properties']['Province'] == prov2:
                    pp['properties']['freq'] = float(row['province_id'])
        disdata_out = province
    return disdata_out

## Function for converting data in list from string to float
# Using for Observation page to convert string list of weather parameter (rainfall, min temp and max temp) to float.
def listConvertDataType(li):
    for i in range(0, len(li)):
        li[i] = float(li[i])
    return li