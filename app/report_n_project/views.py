from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from app.report_n_project.models import sdc_project_cambodia
import io
from reportlab.pdfgen import canvas

from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your views here.
##########################################################################
########################### Upload Data Module ###########################
##########################################################################
def upload_data(request):
    return render(request, "upload_data.html", {'url_name': 'upload_data'})

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
