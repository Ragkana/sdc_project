from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import EarthquakeSerializer, BulletinSerializer, BulletinNoSerializer
from app.earthquake.models import earthquake_events, earthquake_bulletins, earthquake_settings
from urllib.request import urlopen
from app.earthquake import views as eq_views
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json


polygon1 = Polygon([(102.193619,12.43423),(102.083683,13.974383),(102.413492,15.165258),(103.292984,15.927327),(104.632687,16.454854),(105.90795,16.539127),(106.985328,16.222916),(107.513023,15.694773),(108.150846,14.251406),
    (108.304757,12.541494),(108.106871,11.402293),(105.864166,10.517856),(103.929283,9.890731),(102.368024,10.712225),(102.193619,12.43423)])

polygon2 = Polygon([(100.65212,21.787875),(101.267765,21.910241),(101.421676,22.90559),(102.500519,23.107839),(103.797872,21.644983),(105.029161,21.379237),(105.952686,19.733421),(106.722242,17.986897),(107.976642,15.85105),
    (107.976642,14.366178),(106.965226,13.299425),(105.602013,13.299425),(104.018928,13.982712),(104.546623,15.131125),(103.799054,16.863034),(101.952121,17.199178),(100.676857,16.863034),(100.193137,18.245655),(98.562707,19.865539),(100.65212,21.787875)])

polygon3 = Polygon([(98.786447,18.036851),(97.159387,15.977833),(95.268479,15.131125),(92.937824,15.935581),(93.46552,17.785959),(92.058332,19.410259),(91.266789,21.141509),(91.531633,23.418518),(93.774338,25.933965),
    (94.917766,27.504008),(96.896623,28.628528),(99.535099,29.013545),(99.667023,25.101145),(100.060656,23.499144),(101.028098,22.569),(102.127463,20.607721),(98.917316,19.036805),(98.786447,18.036851)])


@api_view(['POST'])
def import_earthquake(request):
    settings = earthquake_settings.objects.first()

    
    if not 'event_id' in request.data:
        return Response({'message':'Event ID is required!'})
    
    event_id = request.data['event_id']
    point = Point(float(request.data['longitude']), float(request.data['latitude']))
    is_inside = polygon1.contains(point) or polygon2.contains(point) or polygon3.contains(point)
    
    if  earthquake_events.objects.filter(pk=request.data['event_id']).exists():
        # Update
        earthquake_event = earthquake_events.objects.get(pk=request.data['event_id'])
        serializer = EarthquakeSerializer(earthquake_event, data=request.data)
    else: # Insert
        serializer = EarthquakeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        # Update if inside
        earthquake_events.objects.filter(pk=request.data['event_id']).update(is_inside = is_inside)

        # send advisory if auto send
        receiver_email = settings.auto_send_email
        if settings.auto_send and is_inside:
            eq_views.prepare_advisory(event_id, receiver_email, 0, 0)

        return Response({'message':'Success!'})
    return Response(serializer.errors)


@api_view(['POST'])
def import_bulletin(request):
    event_id = request.data['event_id']
    bulletin_no = request.data['bulletin_no']
    # p_event_id = 'rm2019paca'
    # p_bulletin_no = '1'    
    url = 'https://www.rimes.int/app/import/get-bulletin.php?event_id=' + event_id + '&bulletin_no=' + bulletin_no

    response = urlopen(url)
    data_json = json.loads(response.read())

    if len(data_json) == 0:
        return Response({'record':'No bulletin found!'})

    del data_json[0]['_usgs_shakecast_url_']

    if  earthquake_bulletins.objects.filter(event_id=event_id, bulletin_no=bulletin_no).exists():
        # Update
        bulletin = earthquake_bulletins.objects.get(event_id=event_id, bulletin_no=bulletin_no)
        serializer = BulletinSerializer(bulletin, data=data_json[0])
    else: # Insert
        serializer = BulletinSerializer(data=data_json[0])

    if serializer.is_valid():
      
        # Update Earthquake bulletin no
        earthquake_event = earthquake_events.objects.get(pk=event_id)
        serializer = BulletinNoSerializer(earthquake_event, data=request.data)
        if serializer.is_valid():
            serializer.save()

        # Get event long lat
        point = Point(earthquake_event.longitude, earthquake_event.latitude)
        is_inside = polygon.contains(point)
       
        # send advisory if auto send
        settings = earthquake_settings.objects.first()
        receiver_email = settings.auto_send_email
        if settings.auto_send and is_inside:
            eq_views.prepare_advisory(event_id, receiver_email, int(bulletin_no), 0)
  
    return Response({'message':'Success!'})

  

