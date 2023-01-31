from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
## import database ##
from app.report_n_project.models import sdc_project_cambodia, sdc_project_laos, country, reports_temporary
from app.disaster_ana.models import sdc_project_location_cambodia, sdc_project_location_laos
from app.disaster_ana.models import disaster
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

## PDF Generator || xhtml2pdf ##
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.contrib.staticfiles import finders

from django.conf import settings
import pandas as pd
import numpy as np
import os

# Create your views here.
##########################################################################
########################### Upload Data Module ###########################
##########################################################################
## Upload data module main page ##
@login_required(login_url='login')
def upload_data(request):
    coun_id, coun_name = "", ""
    prov_name, prov_id = "", ""
    dist_name, dist_id = "", ""
    comm_name, comm_id = "", ""
    day = ""
    haz, death, injured, miss, h_des, h_dam = "", "", "", "", "", ""
    comments = ""
    file_url, dis_data = "", ""

    if request.method=='POST' and 'submit_data' in request.POST:
        ## Retrieve data from form ##
        coun_id = request.POST.get('country_select')
        prov_name = request.POST.get('province_selected')
        dist_name = request.POST.get('district_selected')
        comm_name = request.POST.get('commune_selected')
        day = request.POST.get('selected_date')
        haz = request.POST.get('haz_selected')
        death = request.POST.get('death')
        injured = request.POST.get('injured')
        miss = request.POST.get('missing')
        h_des = request.POST.get('h_des')
        h_dam = request.POST.get('h_dam')
        comments = request.POST.get('comment_box')
        ## Fill all ID columns ##
        # Retrieve country name in string
        coun_name = country.objects.values('country_name').annotate(count=Count('country_name')).filter(country_id=coun_id)
        coun_name = list(coun_name.values_list('country_name', flat=True))[0]
        # Retrieve province id in string
        prov_id = country.objects.values('province_id').annotate(count=Count('province_name')).filter(province_name=prov_name)
        prov_id = list(prov_id.values_list('province_id', flat=True))[0]
        # Retrieve district id in string
        dist_id = country.objects.values('district_id').annotate(count=Count('district_name')).filter(district_name=dist_name)
        dist_id = list(dist_id.values_list('district_id', flat=True))[0]
        # Retrieve commune id in string
        comm_id = country.objects.values('commune_id').annotate(count=Count('commune_name')).filter(commune_name=comm_name)
        comm_id = list(comm_id.values_list('commune_id', flat=True))[0]
        ## Add to disaster database ##
        data = disaster(province_id=prov_id, province_name=prov_name, district_id=dist_id, district_name=dist_name, commune_id=comm_id, commune_name=comm_name,
        date_data=day, event=haz, deaths=death, injured=injured, missing=miss, house_destroy=h_des, house_damage=h_dam, comment=comments)
        data.save()
    if request.method=='POST' and 'upload_file' in request.POST:
        data_csv = request.FILES['disaster_csv']
        # save PDF to specific path
        fss = FileSystemStorage(base_url='static/upload_disaster_data/', location='static/upload_disaster_data/')
        file_path = fss.save(data_csv.name, data_csv)
        # Get the url
        file_url = fss.url(file_path)
        # Open that csv file
        dis_data = pd.read_csv(file_url)
        # Save to database
        SaveToDisData(dis_data)
        
    return render(request, "upload_data.html", {'url_name': 'upload_data', 'url':file_url, 'dataframe':dis_data})

def SaveToDisData(df):
    df['date_data'] = pd.to_datetime(df['date_data'], format = '%Y-%m-%d')
    df = df.fillna('')
    for i in df.index:
        dis_data = disaster(province_id=df['province_id'][i], province_name=df['province_name'][i], district_id=df['district_id'][i], 
        district_name=df['district_name'][i], commune_id=df['commune_id'][i], commune_name=df['commune_name'][i],
        date_data=df['date_data'][i], event=df['event'][i], deaths=df['deaths'][i], injured=df['injured'][i], missing=df['missing'][i], 
        house_destroy=df['houses_destroy'][i], house_damage=df['houses_damage'][i], comment=df['comment'][i])
        dis_data.save()


def country_choose(request):
    country_val = request.POST['country']
    if country_val == 'KHM':
        df = country.objects.values('province_name').annotate(count=Count('province_id')).filter(country_id='KHM')
        province_name = list(df.values_list('province_name', flat=True))
        df2 = disaster.objects.values('event').annotate(count=Count('event')).filter(province_id__startswith='KHM')
        event = list(df2.values_list('event', flat=True))
    if country_val == 'LAO':
        df = country.objects.values('province_name').annotate(count=Count('province_id')).filter(country_id='LAO')
        province_name = list(df.values_list('province_name', flat=True))
        df2 = disaster.objects.values('event').annotate(count=Count('event')).filter(province_id__startswith='LAO')
        event = list(df2.values_list('event', flat=True))

    return JsonResponse({'country':country_val, 'province':province_name, 'event':event})

def province_choose(request):
    province = request.POST['province']
    df = country.objects.values('district_name').annotate(count=Count('district_id')).filter(province_name=province).order_by('district_name')
    df = list(df.values_list('district_name', flat=True))

    return JsonResponse({'province':province, 'district':df})

def district_choose(request):
    district = request.POST['district']
    df = country.objects.values('commune_name').annotate(count=Count('commune_id')).filter(district_name=district)
    df = list(df.values_list('commune_name', flat=True))

    return JsonResponse({'district':district, 'commune':df})

##########################################################################
########################### SDC Project Module ###########################
##########################################################################
## SDC cambodia project main page ##
@login_required(login_url='login')
def sdc_project_khm(request):
    khm_project = sdc_project_cambodia.objects.all()

    if request.method == 'POST' and request.FILES['khm_pdf']:
        ## Retrieve string data
        khm_fullname = request.POST.get('KHM_ProjectName')
        khm_abb_name = request.POST.get('KHM_ProjectABBName')
        khm_obj = request.POST.get('KHM_Objective')
        khm_dur = request.POST.get('KHM_Duration')
        khm_bud = request.POST.get('KHM_Budget')
        khm_loc = request.POST.get('KHM_Location')
        khm_par = request.POST.get('KHM_partners')
        khm_out = request.POST.get('KHM_Outcome')
        ## Retrieve PDF data
        khm_pdf = request.FILES['khm_pdf']
        # save PDF to specific path
        fss = FileSystemStorage(base_url='static/sdc_project_pdf/Cambodia/', location='static/sdc_project_pdf/Cambodia/')
        khm_file = fss.save(khm_pdf.name, khm_pdf)
        # Get the url
        khm_file_url = fss.url(khm_file)
        # cut url string to keep it in database and for use
        khm_file_url = khm_file_url[7:]
        #return render(request, "sdc_project_khm.html", {'khm_url': khm_file_url, 'duration':khm_dur, 'khm_project':khm_project})
        ## Save data to database
        khm_data = sdc_project_cambodia(project_fullname=khm_fullname, project_shortname=khm_abb_name, objective=khm_obj, duration=khm_dur,
         budget=khm_bud, location=khm_loc, partners=khm_par, outcome=khm_out, pdf_download=khm_file_url)
        khm_data.save()
        return HttpResponseRedirect(reverse('sdc_project_cambodia'))
    
    return render(request, "sdc_project_khm.html", {'url_name': 'sdc_project_cambodia', 'khm_project':khm_project})

## SDC Loas Project main page ##
@login_required(login_url='login')
def sdc_project_lao(request):
    lao_project = sdc_project_laos.objects.all()
    if request.method == 'POST' and request.FILES['lao_pdf']:
        ## Retrieve string data
        lao_fullname = request.POST.get('LAO_ProjectName')
        lao_abb_name = request.POST.get('LAO_ProjectABBName')
        lao_obj = request.POST.get('LAO_Objective')
        lao_dur = request.POST.get('LAO_Duration')
        lao_bud = request.POST.get('LAO_Budget')
        lao_loc = request.POST.get('LAO_Location')
        lao_par = request.POST.get('LAO_partners')
        lao_out = request.POST.get('LAO_Outcome')
        ## Retrieve PDF data
        lao_pdf = request.FILES['lao_pdf']
        # save PDF to specific path
        fss = FileSystemStorage(base_url='static/sdc_project_pdf/Laos/', location='static/sdc_project_pdf/Laos/')
        lao_file = fss.save(lao_pdf.name, lao_pdf)
        # Get the url
        lao_file_url = fss.url(lao_file)
        # cut url string to keep it in database and for use
        lao_file_url = lao_file_url[7:]
        #return render(request, "sdc_project_lao.html", {'lao_url': lao_file_url, 'duration':lao_dur, 'lao_project':lao_project})
        ## Save data to database
        lao_data = sdc_project_laos(project_fullname=lao_fullname, project_shortname=lao_abb_name, objective=lao_obj, duration=lao_dur,
         budget=lao_bud, location=lao_loc, partners=lao_par, outcome=lao_out, pdf_download=lao_file_url)
        lao_data.save()
        return HttpResponseRedirect(reverse('sdc_project_laos'))
    
    return render(request, "sdc_project_lao.html", {'url_name': 'sdc_project_laos', 'lao_project':lao_project})

## SDC Project Myanmar Main page ##
@login_required(login_url='login')
def sdc_project_mya(request):
    
    return render(request, "sdc_project_mya.html", {'url_name': 'sdc_project_myanmar'})

## SDC Project location main page ##
@login_required(login_url='login')
def sdc_project_location(request):
    country = ""
    project = ""
    lat = ""
    long = ""
    detail = ""
    if request.method=='POST' and 'submit_data' in request.POST:
        country = request.POST.get('country_selected')
        project = request.POST.get('project_selected')
        lat = request.POST.get('latitude')
        long = request.POST.get('longitude')
        detail = request.POST.get('detail')
        if country == 'KHM':
            c_name = "Cambodia"
            data = sdc_project_location_cambodia(project=project, country_id=country, country_name=c_name, latitude=lat, longitude=long, detail=detail)
            data.save()
        if country == 'LAO':
            c_name = "Laos"
            data = sdc_project_location_laos(project=project, country_id=country, country_name=c_name, latitude=lat, longitude=long, detail=detail)
            data.save()
        if country == 'MYA':
            c_name = "Myanmar"
            #data = sdc_project_location_cambodia(project=project, country_id=country, country_name=c_name, latitude=lat, longitude=long, detail=detail)
            #data.save()
        
    return render(request, "add_project_location.html", {'url_name': 'sdc_project_location'})

def country_project_choose(request):
    country_project = request.POST['country']
    if country_project == 'KHM':
        p_name = list(sdc_project_cambodia.objects.values_list('project_shortname', flat=True))
    if country_project == 'LAO':
        p_name = list(sdc_project_laos.objects.values_list('project_shortname', flat=True))
    if country_project == 'MYA':
        p_name = list()

    return JsonResponse({'project':p_name})



######################################################################
########################### Reports Module ###########################
######################################################################

## Main Page ##
@login_required(login_url='login')
def reports(request):
    country = ""
    hazard = ""
    profile = ""
    haz_p, dis_p, vul_p = "0", "0", "0"
    if request.method=='POST' and 'pdf_gen' in request.POST:
        country = request.POST.get('country_selected')
        hazard = request.POST.get('haz_selected')
        profile = request.POST.getlist('profile')
        for p in profile:
            if p == "hazard_profile":
                haz_p = 1
            if p == "disaster_profile":
                dis_p = 1
            if p == "vulnerability_profile":
                vul_p = 1
        data = reports_temporary(country_id=country, hazard_type=hazard, hazard_p=haz_p, disaster_p=dis_p, vulnerability_p=vul_p)
        data.save()
        return HttpResponseRedirect('reports/reports_pdf')

    return render(request, "report/reports.html", {'url_name': 'reports'})

def country_event(request):
    country_val = request.POST['country']
    if country_val == 'KHM':
        df = disaster.objects.values('event').annotate(count=Count('event')).filter(province_id__startswith='KHM')
        event = list(df.values_list('event', flat=True))
    if country_val == 'LAO':
        df = disaster.objects.values('event').annotate(count=Count('event')).filter(province_id__startswith='LAO')
        event = list(df.values_list('event', flat=True))
    if country_val == 'MYA':
        df = disaster.objects.values('event').annotate(count=Count('event')).filter(province_id__startswith='MYA')
        event = list(df.values_list('event', flat=True))

    return JsonResponse({'country':country_val, 'event':event})

## PDF Generator ##
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """
    result = finders.find(uri)
    if result:
        if not isinstance(result, (list, tuple)):
            result = [result]
        result = list(os.path.realpath(path) for path in result)
        path=result[0]
    else:
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

def html_to_pdf(request):
    template_path = 'report/report_pdf_template.html'
    ## Send data to template ##
    data = reports_temporary.objects.values('country_id', 'hazard_type', 'hazard_p', 'disaster_p', 'vulnerability_p').last()
    country = data['country_id']
    country_name = country_trans(country)
    event = data['hazard_type']
    hazard_p = data['hazard_p']
    disaster_p = int(data['disaster_p'])
    vul_p = int(data['vulnerability_p'])

    hprov_ys, hprov_ye = "", ""
    hdist_ys, hdist_ye = "", ""
    hcomm_ys, hcomm_ye = "", ""

    ## Hazard Profile ##
    if country == "KHM":
        haz_province = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(province_id__startswith='KHM'))
        haz_district = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(district_id__startswith='KHM'))
        haz_commune = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(commune_id__startswith='KHM'))
    if country == "LAO":
        haz_province = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(province_id__startswith='LAO'))
        haz_district = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(district_id__startswith='LAO'))
    if country == "MYA":
        haz_province = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(province_id__startswith='MYA'))
        haz_district = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(district_id__startswith='MYA'))
        haz_commune = pd.DataFrame(disaster.objects.values('province_id','province_name','district_id','district_name', 'commune_id','commune_name','date_data','event').filter(commune_id__startswith='MYA'))

    # Add year 
    if country == "KHM" or country == "MYA":
        haz_province['year'] = pd.DatetimeIndex(haz_province['date_data']).year
        haz_district['year'] = pd.DatetimeIndex(haz_district['date_data']).year
        haz_commune['year'] = pd.DatetimeIndex(haz_commune['date_data']).year
        # Filter by hazard selection
        haz_province = haz_province[haz_province['event']==event]
        haz_district = haz_district[haz_district['event']==event]
        haz_commune = haz_commune[haz_commune['event']==event]
        # Get max-Min Year
        hprov_ys = int(haz_province['year'].min())
        hprov_ye = int(haz_province['year'].max())

        hdist_ys = int(haz_district['year'].min())
        hdist_ye = int(haz_district['year'].max())

        hcomm_ys = int(haz_commune['year'].min())
        hcomm_ye = int(haz_commune['year'].max())
    if country == "LAO":
        haz_province['year'] = pd.DatetimeIndex(haz_province['date_data']).year
        haz_district['year'] = pd.DatetimeIndex(haz_district['date_data']).year
        # Filter by hazard selection
        haz_province = haz_province[haz_province['event']==event]
        haz_district = haz_district[haz_district['event']==event]
        # Get max-Min Year
        hprov_ys = int(haz_province['year'].min())
        hprov_ye = int(haz_province['year'].max())

        hdist_ys = int(haz_district['year'].min())
        hdist_ye = int(haz_district['year'].max())

    event_n = event
    # Event name change
    if event_n == 'COLD WAVE':
        event_n = 'COLDWAVE'
    if event_n == 'FLASH FLOOD':
        event_n = 'FLASHFLOOD'
    if event_n == 'RIVER BANK COLLAPSE':
        event_n = 'RIVERBANKCOLLAPSE'
    
    # Hazard image
    haz_prov_img = "images/report_img/" + country + "/hazard_profile/" + country + "_" + event_n + "_Province.jpg"
    haz_dist_img = "images/report_img/" + country + "/hazard_profile/" + country + "_" + event_n + "_District.jpg"
    haz_comm_img = "images/report_img/" + country + "/hazard_profile/" + country + "_" + event_n + "_Commune.jpg"

    ## Disaster Profile ##
    # Deaths #
    # map
    dis_prov_d_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_deaths_Province.jpg"
    dis_dist_d_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_deaths_District.jpg"
    dis_comm_d_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_deaths_Commune.jpg"
    # Bar
    dis_prov_d_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_deaths_Province.png"
    dis_dist_d_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_deaths_District.png"
    dis_comm_d_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_deaths_Commune.png"
    # Annual
    dis_ann_d = "images/report_img/" + country + "/disaster_profile/annual/" + country + "_" + event_n + "_deaths.png"

    # Injury #
    # Map
    dis_prov_i_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_injured_Province.jpg"
    dis_dist_i_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_injured_District.jpg"
    dis_comm_i_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_injured_Commune.jpg"
    # Bar 
    dis_prov_i_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_injured_Province.png"
    dis_dist_i_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_injured_District.png"
    dis_comm_i_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_injured_Commune.png"
    # Annual
    dis_ann_i = "images/report_img/" + country + "/disaster_profile/annual/" + country + "_" + event_n + "_injured.png"

    # Missing #
    # Map
    dis_prov_m_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_missing_Province.jpg"
    dis_dist_m_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_missing_District.jpg"
    dis_comm_m_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_missing_Commune.jpg"
    # Bar
    dis_prov_m_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_missing_Province.png"
    dis_dist_m_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_missing_District.png"
    dis_comm_m_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_missing_Commune.png"
    # Annual
    dis_ann_m = "images/report_img/" + country + "/disaster_profile/annual/" + country + "_" + event_n + "_missing.png"

    # houses destroyed #
    # Map
    dis_prov_hdt_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_house_destroy_Province.jpg"
    dis_dist_hdt_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_house_destroy_District.jpg"
    dis_comm_hdt_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_house_destroy_Commune.jpg"
    # Bar
    dis_prov_hdt_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_house_destroy_Province.png"
    dis_dist_hdt_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_house_destroy_District.png"
    dis_comm_hdt_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_house_destroy_Commune.png"
    # Annual
    dis_ann_hdt = "images/report_img/" + country + "/disaster_profile/annual/" + country + "_" + event_n + "_house_destroy.png"

    # houses damage #
    # Map
    dis_prov_hdm_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_house_damage_Province.jpg"
    dis_dist_hdm_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_house_damage_District.jpg"
    dis_comm_hdm_img =  "images/report_img/" + country + "/disaster_profile/map/" + country + "_" + event_n + "_house_damage_Commune.jpg"
    # Bar
    dis_prov_hdm_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_house_damage_Province.png"
    dis_dist_hdm_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_house_damage_District.png"
    dis_comm_hdm_bar =  "images/report_img/" + country + "/disaster_profile/bar/" + country + "_" + event_n + "_house_damage_Commune.png"
    # Annual
    dis_ann_hdm = "images/report_img/" + country + "/disaster_profile/annual/" + country + "_" + event_n + "_house_damage.png"

    ## Disaster Profile ##
    # Population
    vul_pop_size = "images/report_img/" + country + "/vul_profile/population/pop_size.png"
    vul_pop_mpi = "images/report_img/" + country + "/vul_profile/population/pop_mpi.png"
    # MPI
    vul_mpi_mpi = "images/report_img/" + country + "/vul_profile/mpi/mpi.png"
    vul_mpi_pop = "images/report_img/" + country + "/vul_profile/mpi/mpi_pop.png"
    vul_mpi_in = "images/report_img/" + country + "/vul_profile/mpi/mpi_in.png"
    vul_mpi_se = "images/report_img/" + country + "/vul_profile/mpi/mpi_se.png"
    vul_mpi_vul = "images/report_img/" + country + "/vul_profile/mpi/mpi_vul.png"

    context = {'event':event, 'country':country_name, 'hazard_p':hazard_p, 'disaster_p':disaster_p, 'vulnerability_p':vul_p, 'hprov_ys':hprov_ys, 
    'hprov_ye':hprov_ye, 'hdist_ys':hdist_ys, 'hdist_ye':hdist_ye, 'hcomm_ys':hcomm_ys, 'hcomm_ye':hcomm_ye, 'haz_prov_img':haz_prov_img, 
    'haz_dist_img':haz_dist_img, 'haz_comm_img':haz_comm_img, 'dis_prov_d_img':dis_prov_d_img, 'dis_dist_d_img':dis_dist_d_img, 'dis_comm_d_img':dis_comm_d_img,
    'dis_prov_i_img':dis_prov_i_img, 'dis_dist_i_img':dis_dist_i_img, 'dis_comm_i_img':dis_comm_i_img, 'dis_prov_m_img':dis_prov_m_img, 
    'dis_dist_m_img':dis_dist_m_img, 'dis_comm_m_img':dis_comm_m_img, 'dis_prov_hdt_img':dis_prov_hdt_img, 'dis_dist_hdt_img':dis_dist_hdt_img,
     'dis_comm_hdt_img':dis_comm_hdt_img, 'dis_prov_hdm_img':dis_prov_hdm_img, 'dis_dist_hdm_img':dis_dist_hdm_img, 'dis_comm_hdm_img':dis_comm_hdm_img,
     
     'dis_prov_d_bar':dis_prov_d_bar, 'dis_dist_d_bar':dis_dist_d_bar, 'dis_comm_d_bar':dis_comm_d_bar,
    'dis_prov_i_bar':dis_prov_i_bar, 'dis_dist_i_bar':dis_dist_i_bar, 'dis_comm_i_bar':dis_comm_i_bar, 'dis_prov_m_bar':dis_prov_m_bar, 
    'dis_dist_m_bar':dis_dist_m_bar, 'dis_comm_m_bar':dis_comm_m_bar, 'dis_prov_hdt_bar':dis_prov_hdt_bar, 'dis_dist_hdt_bar':dis_dist_hdt_bar,
     'dis_comm_hdt_bar':dis_comm_hdt_bar, 'dis_prov_hdm_bar':dis_prov_hdm_bar, 'dis_dist_hdm_bar':dis_dist_hdm_bar, 'dis_comm_hdm_bar':dis_comm_hdm_bar,
     
     'dis_ann_d':dis_ann_d, 'dis_ann_i':dis_ann_i, 'dis_ann_m':dis_ann_m, 'dis_ann_hdt':dis_ann_hdt, 'dis_ann_hdm':dis_ann_hdm,

     'vul_pop_size':vul_pop_size, 'vul_pop_mpi':vul_pop_mpi, 'vul_mpi_mpi':vul_mpi_mpi, 'vul_mpi_vul':vul_mpi_vul, 'vul_mpi_pop':vul_mpi_pop,
     'vul_mpi_in':vul_mpi_in, 'vul_mpi_se':vul_mpi_se}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="SDC_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

## Change country_id to full name
def country_trans(country):
    if country == 'KHM':
        result = 'Cambodia'
    if country == 'LAO':
        result = 'Laos'
    if country == 'MYA':
        result = 'Myanmar'
    return result

#######################################################################
########################### About us Module ###########################
#######################################################################
## Main Page ##
@login_required(login_url='login')
def about_sdc(request):
    return render(request, "about_sdc.html", {'url_name': 'about_sdc'})

