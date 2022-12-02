from enum import auto
from itertools import count
from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse, HttpResponseRedirect, HttpResponse
from django.urls import reverse
## import database ##
from app.report_n_project.models import sdc_project_cambodia, sdc_project_laos, country
from app.disaster_ana.models import sdc_project_location_cambodia, sdc_project_location_laos
from app.disaster_ana.models import disaster
import io
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required, permission_required

## PDF Generator || reportlab ##
from django.core.files.storage import FileSystemStorage
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4 # 210*270 mm
from reportlab.lib.units import mm
from io import BytesIO
## PDF Generator || xhtml2pdf ##
from xhtml2pdf import pisa
from django.template.loader import get_template

from django.conf import settings
import pandas as pd
import numpy as np


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
    return render(request, "reports.html", {'url_name': 'reports'})

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
def report_pdf(request):
    country = ""
    if request.method=='POST' in request.POST:
        ## Retrieve data from form ##
        country = request.POST.get('country_select')

    buffer = io.BytesIO()
    report = canvas.Canvas(buffer, pagesize=A4)
    
    ## Title :: set font ##
    # Set title name that will show in browser.
    report.setTitle("SDC reports")
    # Set title name that will show in document
    report.drawString(100, 100, "Test for Reports.")
    # set font style and size for pdf
    report.set_font('Arial', size= 16)
    report.drawString(100, 10, country + " Test")
    
    ## Template :: Draw top & bottom gradient image ##
    # Banner Top
    report.drawInlineImage('static/images/report_img/sdc_template.png', x=0, y=272*mm, width=210*mm, height=25*mm)
    # Banner Bottom
    report.drawInlineImage('static/images/report_img/sdc_template.png', x=0, y=0, width=210*mm, height=25*mm)
    # SDC logo
    report.drawImage('static/images/report_img/swiss-logo.png', x=460, y=775, width=45*mm, height=25*mm)
    drawMyRuler(report)
    report.showPage()
    report.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='report_test.pdf')


## Draw ruler in pdf 
def drawMyRuler(pdf):
    pdf.drawString(100,810, 'x100')
    pdf.drawString(200,810, 'x200')
    pdf.drawString(300,810, 'x300')
    pdf.drawString(400,810, 'x400')
    pdf.drawString(500,810, 'x500')

    pdf.drawString(10,100, 'y100')
    pdf.drawString(10,200, 'y200')
    pdf.drawString(10,300, 'y300')
    pdf.drawString(10,400, 'y400')
    pdf.drawString(10,500, 'y500')
    pdf.drawString(10,600, 'y600')
    pdf.drawString(10,700, 'y700')
    pdf.drawString(10,800, 'y800')




#######################################################################
########################### About us Module ###########################
#######################################################################
## Main Page ##
@login_required(login_url='login')
def about_sdc(request):
    return render(request, "about_sdc.html", {'url_name': 'about_sdc'})

