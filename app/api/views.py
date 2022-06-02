from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import EarthquakeSerializer, BulletinSerializer, BulletinNoSerializer
from app.earthquake.models import earthquake_events, earthquake_bulletins, earthquake_settings
from urllib.request import urlopen
from app.earthquake import views as eq_views
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import json

polygon = Polygon([(72.268492,39.827522), (80.182943,40.096983), (92.671651,33.927409), (109.030101,20.202924),
        (115.010609,-7.294363), (105.16036,-14.368173), (85.108067,-14.02735), (64.879645,-12.315853), 
        (58.371445,7.081814), (61.361699,32.159338), (72.268492,39.827522)])

@api_view(['POST'])
def import_earthquake(request):
    
    if not 'event_id' in request.data:
        return Response({'message':'Event ID is required!'})
    
    event_id = request.data['event_id']
    point = Point(float(request.data['longitude']), float(request.data['latitude']))
    is_inside = polygon.contains(point)

    print(polygon.contains(point))

    if  earthquake_events.objects.filter(pk=request.data['event_id']).exists():
        # Update
        earthquake_event = earthquake_events.objects.get(pk=request.data['event_id'])
        serializer = EarthquakeSerializer(earthquake_event, data=request.data)
    else: # Insert
        serializer = EarthquakeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        # send advisory if auto send
        settings = earthquake_settings.objects.first()
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

  

