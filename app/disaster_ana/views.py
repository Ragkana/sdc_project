from datetime import date
from multiprocessing.sharedctypes import Value
from traceback import StackSummary
from django.forms import IntegerField
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Avg, Count, Sum
from app.disaster_ana.models import disaster
from django.db.models import F

import json
import pandas as pd


# Create your views here.
def hazard_ana(request):
    # Sending disaster type value
    haz_event = disaster.objects.values('event').annotate(count=Count('event'))
    # Retrieve data from template
    khm_hazard_selected = request.POST.get('khm_haz_selected')
    khm_level_selected = request.POST.get('khm_level_selected')

    ## Set default value ##
    if khm_hazard_selected == None and khm_level_selected == None :
        khm_hazard_selected = 'DROUGHT'
        khm_level_selected = 'province_name'
    else:
        khm_hazard_selected = khm_hazard_selected
        khm_level_selected = khm_level_selected

    ## Create Hazard DataFrame for each country ##
    khm_hazard_df = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name',
    'commune_id','commune_name','date_data','event').filter(province_id__startswith='KHM'))
    # Add year 
    khm_hazard_df['year'] = pd.DatetimeIndex(khm_hazard_df['date_data']).year
    # Filter by hazard selection
    khm_hazard_df = khm_hazard_df[khm_hazard_df['event']==khm_hazard_selected]
    # Get max-Min Year
    year_start = khm_hazard_df['year'].min()
    year_end = khm_hazard_df['year'].max()
    # Group by and sum hazard in each area
    khm_df = khm_hazard_df.groupby(khm_level_selected).count()

    ## Load GeoJson map ##
    return render(request, "hazard_ana.html", {'url_name': 'hazard_ana', 'haz_event':haz_event, 'hazard_param':khm_hazard_selected, 'level_param':khm_level_selected,
    'year_start':year_start, 'year_end':year_end, 'test':khm_df})

def disaster_ana(request):
    # Retrieve data from template
    disaster_selected = request.POST.get('dis_selected')
    impact_selected = request.POST.get('impact_selected')
    level_selected = request.POST.get('level_selected')

    dis_event = disaster.objects.values('event').annotate(count=Count('event'))

    # Set default value
    if impact_selected == None and disaster_selected == None and level_selected == None:
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
""""
    # Extract year from date column
    #dis_year = disaster.objects.all().extra(select={'year': "EXTRACT(year FROM date)"}).values('year').annotate(count_items=Count('date'))
    dis_year = dis_qs.values('year', 'event').annotate(impact=Sum(impact_selected)).filter(event=disaster_selected)
    df_year_data = pd.DataFrame(dis_year)

    list_year = df_year_data['year'].tolist()
    list_year = [float(f) for f in list_year]
    list_impact = df_year_data['impact'].tolist()

    return render(request, "disaster_ana.html", {'url_name': 'disaster_ana', 'disaster_param':disaster_selected, 
    'impact_param': impact_selected, 'level_param': level_selected, 'dis_event':dis_event, '4year':df_year_data, 
    'map_data':map_sum, 'level_code':code, 'level_value':value, 'list_year':list_year, 'list_impact':list_impact})
    """

    