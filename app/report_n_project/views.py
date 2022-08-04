from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from app.report_n_project.models import sdc_project_cambodia, sdc_project_laos
from app.disaster_ana.models import disaster
import io
from reportlab.pdfgen import canvas
from django.db.models import Count

from django.core.files.storage import FileSystemStorage
from django.conf import settings
import pandas as pd

# Create your views here.
##########################################################################
########################### Upload Data Module ###########################
##########################################################################
def upload_data(request):
    date = request.POST.get('selected_date')
    
    return render(request, "upload_data.html", {'url_name': 'upload_data'})

def country_choose(request):
    country = request.POST['country']
    if country == 'KHM':
        df = disaster.objects.values('province_id','province_name').annotate(count=Count('province_id')).filter(province_id__startswith='KHM')
        df = list(df.values_list('province_name', flat=True))
    if country == 'LAO':
        df = disaster.objects.values('province_id','province_name').annotate(count=Count('province_id')).filter(province_id__startswith='LAO')
        df = list(df.values_list('province_name', flat=True))

    return JsonResponse({'country':country, 'province':df})

##########################################################################
########################### SDC Project Module ###########################
##########################################################################
def sdc_project(request):
    khm_project = sdc_project_cambodia.objects.all()
    
    return render(request, "sdc_project.html", {'url_name': 'sdc_project', 'khm_project':khm_project})

def sdc_project_khm(request):
    khm_project = sdc_project_cambodia.objects.all()

    if request.method == 'POST' and request.FILES['khm_pdf']:
        ## Retrieve string data
        khm_name = request.POST.get('KHM_ProjectName')
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
        khm_data = sdc_project_cambodia(project_name=khm_name, objective=khm_obj, duration=khm_dur,
         budget=khm_bud, location=khm_loc, partners=khm_par, outcome=khm_out, pdf_download=khm_file_url)
        khm_data.save()
        return HttpResponseRedirect(reverse('sdc_project_cambodia'))
    
    return render(request, "sdc_project_khm.html", {'url_name': 'sdc_project_cambodia', 'khm_project':khm_project})

def sdc_project_lao(request):
    lao_project = sdc_project_laos.objects.all()
    if request.method == 'POST' and request.FILES['lao_pdf']:
        ## Retrieve string data
        lao_name = request.POST.get('LAO_ProjectName')
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
        lao_data = sdc_project_laos(project_name=lao_name, objective=lao_obj, duration=lao_dur,
         budget=lao_bud, location=lao_loc, partners=lao_par, outcome=lao_out, pdf_download=lao_file_url)
        lao_data.save()
        return HttpResponseRedirect(reverse('sdc_project_laos'))
    
    return render(request, "sdc_project_lao.html", {'url_name': 'sdc_project_laos', 'lao_project':lao_project})

def sdc_project_mya(request):
    
    return render(request, "sdc_project_mya.html", {'url_name': 'sdc_project_myanmar'})

def khm_add_project(request):
    khm_name = request.POST['khm_name']
    khm_obj = request.POST['khm_obj']
    khm_dur = request.POST['khm_dur']
    khm_bud = request.POST['khm_bud']
    khm_loc = request.POST['khm_loc']
    khm_par = request.POST['khm_par']
    khm_out = request.POST['khm_out']
    

    return JsonResponse({'name':khm_name, 'obj':khm_obj, 'dur':khm_dur, 'bud':khm_bud, 'loc':khm_loc, 'par':khm_par, 'out':khm_out}, status=200)
    """
    if request.method == 'POST' and request.FILES['khm_pdf']:
        khm_pdf = request.FILES['khm_pdf']
        fss = FileSystemStorage(base_url='static/sdc_project_pdf/Cambodia/', location='static/sdc_project_pdf/Cambodia/')
        khm_file = fss.save(khm_pdf.name, khm_pdf)
        khm_file_url = fss.url(khm_file)
        return render(request, "sdc_project.html", {'khm_url': khm_file_url})
        """

######################################################################
########################### Reports Module ###########################
######################################################################

## Main Page ##
def reports(request):
    return render(request, "reports.html", {'url_name': 'reports'})

## PDF Generator ##
def report_pdf(request):
    buffer = io.BytesIO()
    report = canvas.Canvas(buffer)
    report.drawString(100, 100, "Test for Reports.")
    report.showPage()
    report.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='report_test.pdf')
