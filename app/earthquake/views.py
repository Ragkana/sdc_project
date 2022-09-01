from fileinput import filename
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import earthquake_bulletins, earthquake_events, earthquake_settings
from django.core.serializers import serialize
from django.conf import settings
import json
import time
import html

# For Email
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# For PDF
from io import BytesIO
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

# For login
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def earthquake(request):
   
    eq_settings = earthquake_settings.objects.all()
    num_events = eq_settings[0].number_events

    filter = ""
    filter_mag = ""
    filter_aoi = ""

    if (eq_settings[0].filter_1):
        filter_mag += ("" if filter_mag == "" else " or ") + " magnitude < 5"
    if (eq_settings[0].filter_2):
        filter_mag += ("" if filter_mag == "" else " or ") + " (magnitude >= 5 and magnitude < 6)"
    if (eq_settings[0].filter_3):
        filter_mag += ("" if filter_mag == "" else " or ")  + " (magnitude >= 6 and magnitude < 6.5)"
    if (eq_settings[0].filter_4):
        filter_mag += ("" if filter_mag == "" else " or ") + " magnitude >= 6.5"

    if (eq_settings[0].inside_aoi):
        filter_aoi = ("" if filter_mag == "" else " and ") +  " is_inside = 1"

    if (filter_mag != ""):
        filter = '(' + filter_mag + ')'

    filter += filter_aoi

    # earthquakes = earthquake_events.objects.order_by("-event_datetime")[:num_events]
    earthquakes = earthquake_events.objects.raw("SELECT * FROM earthquake_events WHERE " + filter + " ORDER BY event_datetime DESC")[:num_events]
    earthquakes =  serialize('json', earthquakes, fields=['event_id', 'latitude',
         'longitude', 'magnitude', 'phase_count','mag_type', 'depth', 'event_datetime','region', 'bulletin_no',
         'status','is_fake', 'is_inside', 'is_inside', 'is_inside'])

    eheatpoints = earthquake_events.objects.all()
    eheatpoints =  serialize('json', eheatpoints, fields=['latitude',
         'longitude', 'magnitude'])

    PUSHER =  { 
        'KEY': settings.PUSHER['KEY'],
        'CLUSTER': settings.PUSHER['CLUSTER'],
        'CHANNEL': settings.PUSHER['CHANNEL'],
        'EVENT': settings.PUSHER['EVENT'],
    }

    eq_settings =  serialize('json', eq_settings, fields=['simulation', 'number_events',
        'auto_send', 'filter_1', 'filter_2','filter_3', 'filter_4', 'points1','points2', 'points3',
        'inside_aoi', 'show_aor', 'show_aoi', 'show_heatmap', 'auto_send_email'])

    return render(request, "earthquake/earthquake.html", {'url_name': 'earthquake', 'earthquakes' : earthquakes, 'eheatpoints' : eheatpoints , 'settings' : eq_settings, 'PUSHER' : PUSHER })

@login_required(login_url='login')
def setting(request):
    settings = earthquake_settings.objects.first()

    if request.method == 'POST':
        # simulation = True
        # if 'number' not in request.POST:
        #         simulation = False;
        # settings = earthquake_settings.objects.get(pk=1)

        # settings.simulation = True if request.POST['simulation'] == "On" else False
        if  request.POST.get('section', False) == 'earthquake':
            settings.simulation = False  if 'simulation' not in request.POST else True
            settings.auto_send = False  if 'auto_send' not in request.POST else True
            settings.number_events = request.POST['number_events']
            settings.auto_send_email = request.POST['emails']
            settings.save()

        if  request.POST.get('section', False)== 'filter':
            settings.filter_1 = False  if 'filter_1' not in request.POST else True
            settings.filter_2 = False  if 'filter_2' not in request.POST else True
            settings.filter_3 = False  if 'filter_3' not in request.POST else True
            settings.filter_4 = False  if 'filter_4' not in request.POST else True
            settings.inside_aoi = False  if 'inside_aoi' not in request.POST else True
            settings.save()

        if  request.POST.get('section', False) == 'boundaries':
            settings.show_aor = False  if 'show_aor' not in request.POST else True
            settings.show_aoi = False  if 'show_aoi' not in request.POST else True
            settings.show_heatmap = False  if 'show_heatmap' not in request.POST else True
            settings.save()

    return render(request, "earthquake/setting.html", {'url_name': 'earthquake_setting', 'settings' : settings})

def send_advisory(request):
    status = 200

    receiver_email = request.POST['send_to']
    event_id = request.POST['event_id']
    bulletin_no = 0  if 'bulletin_no' not in request.POST else int(request.POST['bulletin_no'])
    simulation = 1 if request.POST['simulation']  == 'true' else 0

    prepare_advisory(event_id, receiver_email, bulletin_no, simulation)

    return JsonResponse({"email": "email sent"}, status=status)

def filter_earthquake(request):

    eq_settings = earthquake_settings.objects.all()
    num_events = eq_settings[0].number_events

    filter = ""
    filter_mag = ""
    filter_aoi = ""

    if (request.POST['filter1'] == "true"):
        filter_mag += ("" if filter_mag == "" else " or ") + " magnitude < 5"
    if ( request.POST['filter2']== "true"):
        filter_mag += ("" if filter_mag == "" else " or ") + " (magnitude >= 5 and magnitude < 6)"
    if (request.POST['filter3']== "true"):
        filter_mag += ("" if filter_mag == "" else " or ")  + " (magnitude >= 6 and magnitude < 6.5)"
    if (request.POST['filter4']== "true"):
        filter_mag += ("" if filter_mag == "" else " or ") + " magnitude >= 6.5"

    if (request.POST['only_aoi']== "true"):
        filter_aoi = ("" if filter_mag == "" else " and ") +  " is_inside = 1"

    if (filter_mag != ""):
        filter = '(' + filter_mag + ')'

    filter += filter_aoi
    

    earthquakes = earthquake_events.objects.raw("SELECT * FROM earthquake_events WHERE " + filter + " ORDER BY event_datetime DESC")[:num_events]
    earthquakes =  serialize('json', earthquakes, fields=['event_id', 'latitude',
         'longitude', 'magnitude', 'phase_count','mag_type', 'depth', 'event_datetime','region', 'bulletin_no',
         'status','is_fake', 'is_inside', 'is_inside', 'is_inside'])

    return JsonResponse({"earthquakes": earthquakes}, status=200)


def view_bulletin(request ,event_id, bulletin_no):

    data = prepare_bulletin_data(event_id, bulletin_no, 0)

    pdf = render_to_pdf('earthquake/bulletin/template.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def prepare_bulletin_data(event_id, bulletin_no, simulation):

    bulletin = earthquake_bulletins.objects.get(event_id = event_id, bulletin_no = bulletin_no)

    param = {}

    # $bulletin_param = $bulletin_param[0];
    bulletin_body = json.loads(bulletin._body)
    param['simulation'] = simulation
    param['org'] = settings.BULLETIN['ORGANIZATION']
    param['eqinfo']   = (bulletin_body['_eqinfo']).replace("//n/","\n")
    param['title'] = bulletin_body['_title']
    param['eqinfo_title_print'] = bulletin_body['_eqinfo_title_print']
    param['eval_title_print']  = bulletin_body['_eval_title_print']
    param['w_threat'] = bulletin_body['w_threat']
    param['threat_title_print'] = bulletin_body['_threat_title_print']
    param['threat'] = bulletin_body['_threat']
    param['w_advice'] = bulletin_body['w_advice']
    param['advice_title_print'] = bulletin_body['_advice_title_print']
    param['advice'] = bulletin_body['_advice']
    param['w_update'] =bulletin_body['w_update']
    param['update_title_print'] =bulletin_body['_update_title_print']
    param['update'] = bulletin_body['_update']
    param['contact_title'] = bulletin_body['_contact_title']
    param['contact_title_print'] = bulletin_body['_contact_title_print']
    param['contact'] = bulletin_body['_contact'].replace("//n/","\n")


    cupdate = '' if bulletin_body['_update_no'] == '0' else ' - Update No. ' + bulletin_body['_update_no'].zfill(3)
    ctype = '' if (bulletin_body['_type']).strip() == '' else ' (' + bulletin_body['_type'] + ')'
 
    param['header1'] = settings.BULLETIN['ORG_SHORT'] + '-' + time.strftime("%Y%m%d-%H%M", time.gmtime()) + '-'+ bulletin_body['_update_no'].zfill(3) + ctype + cupdate
    param['header2'] = 'TSUNAMI BULLETIN NUMBER ' + str(bulletin.bulletin_no) if  bulletin_body['_is_tsu']  else 'EARTHQUAKE BULLETIN'
    param['header3'] = 'Issued at ' +  time.strftime('%H%M', time.gmtime()) + ' UTC ' + time.strftime('%A %d %B %Y', time.gmtime())


    param['header2']  = 'TEST BULLETIN ' + param['header2'] if simulation else param['header2']
    param['test'] =  'TEST ' * 15 if simulation else '' + '\n'
    param['line_break'] =  '-' * 89

    # Precise Info
    bulletin_body['eval']   = (bulletin_body['_eval']).replace('*PRECISE_DATA', bulletin._precise_info) if bulletin._precise_info is not None else bulletin_body['_eval']
    bulletin_body['threat'] = (bulletin_body['_threat']).replace('*PRECISE_DATA', bulletin._precise_info) if bulletin._precise_info is not None else bulletin_body['_threat']
    bulletin_body['advice'] = (bulletin_body['_advice']).replace('*PRECISE_DATA', bulletin._precise_info)  if bulletin._precise_info is not None else bulletin_body['_advice']
    bulletin_body['update'] = (bulletin_body['_update']).replace('*PRECISE_DATA', bulletin._precise_info)  if bulletin._precise_info is not None else bulletin_body['_update']

    # Sea Level Info
    bulletin_body['eval']   = (bulletin_body['_eval']).replace('*PRECISE_DATA', bulletin._sealvl_info) if bulletin._sealvl_info is not None else bulletin_body['_eval']
    bulletin_body['threat'] = (bulletin_body['_threat']).replace('*PRECISE_DATA', bulletin._sealvl_info) if bulletin._sealvl_info is not None else bulletin_body['_threat']
    bulletin_body['advice'] = (bulletin_body['_advice']).replace('*PRECISE_DATA', bulletin._sealvl_info) if bulletin._sealvl_info is not None else bulletin_body['_advice']
    bulletin_body['update'] = (bulletin_body['_update']).replace('*PRECISE_DATA', bulletin._sealvl_info) if bulletin._sealvl_info is not None else bulletin_body['_update']

    param['eval']   = (bulletin_body['_eval']).replace('//n/', '\n')
    param['threat']  = (bulletin_body['_threat']).replace('//n/', '\n')
    param['advice']  = (bulletin_body['_advice']).replace('//n/', '\n')
    param['update']  = (bulletin_body['_update']).replace('//n/', '\n')

    # Cleanup
    param['eval']      = param['eval'].replace('Further information on this event will be available at:', '')
    param['eval']      = param['eval'].replace('http://www.rimes.int/eqt-tsunami-bulletin/', '')
    param['eval']      = param['eval'].replace('http://www.rimes.int/eqt-tsunami-bulletin', '')
    param['eval']      = param['eval'].replace('\n', '')

    for attr in param:
        param[attr] = html.unescape(str(param[attr]).replace('RIMES', settings.BULLETIN['ORG_SHORT']))

    return param


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

def save_pdf(template_src, context_dict={}, filename = ''):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    file = open(filename, "w+b")
    pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file, encoding='utf-8')
    if not pisaStatus.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def prepare_advisory(event_id, receiver_email, bulletin_no, simulation):
    earthquake = earthquake_events.objects.get(pk = event_id)
    subject = 'Earthquake Advisory'
    bulletin_link = ''

    message = MIMEMultipart("alternative")
    if simulation:
        message["Subject"] = '[TEST]' + subject + '[TEST]'
    else:
         message["Subject"] = subject
    
    receiver_email = receiver_email.split(",")

    message["From"] = settings.EMAIL['NAME']  +  '<' + settings.EMAIL['FROM'] + '>'
    message["To"] = ", ".join(receiver_email)
   

    if bulletin_no > 0:
        bulletin_link = '<br/><a href="http://sdc.rimes.int/earthquake/view-bulletin/' + str(event_id) + '/' + str(bulletin_no) + '">View Bulletin</a><br/>'

        # Generate and attached bulletin
        filename = event_id + '_' + str(bulletin_no) + '.pdf'
        filenamepath = settings.BULLETIN['directory'] + filename
        
        data = prepare_bulletin_data(event_id, bulletin_no, simulation)
        save_pdf('earthquake/bulletin/template.html', data, filenamepath)
        
        # Open file in binary mode
        with open(filenamepath, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)

    # Create the plain-text and HTML version of your message
    msg = """\
        <html>
            <body>
            Origin Time = {origin} UTC <br/>
            Magnitude = {mag} Depth = {depth} km. <br/>
            Longitude = {longitude} Latitude = {latitude} <br/>
            Region = {region} <br/>
            {bulletin}
            <br/>Message sent by {org} Automatic Alerting
            
            </body>
        </html>
        """.format(origin=earthquake.event_datetime, mag=earthquake.magnitude, depth=earthquake.depth, 
            longitude=earthquake.longitude, latitude=earthquake.latitude, region=earthquake.region, org=settings.BULLETIN['ORG_SHORT'],
            bulletin=bulletin_link)

    # Turn these into plain/html MIMEText objects
    html = MIMEText(msg, "html")

    message.attach(html)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(settings.EMAIL['HOST'], settings.EMAIL['PORT'], context=context) as server:
        server.login(settings.EMAIL['USER'], settings.EMAIL['PASSWORD'])
        server.sendmail(settings.EMAIL['FROM'], receiver_email, message.as_string())
