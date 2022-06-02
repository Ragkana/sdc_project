from turtle import update
from attr import fields
from rest_framework import serializers
from app.earthquake.models import earthquake_events, earthquake_bulletins
class EarthquakeSerializer(serializers.ModelSerializer):
    class Meta:
            model = earthquake_events
            fields = ('event_id','latitude','longitude','phase_count','magnitude','mag_type','depth','event_datetime','region')

class BulletinNoSerializer(serializers.ModelSerializer):
    class Meta:
            model = earthquake_events
            fields = ('event_id','bulletin_no')

class BulletinSerializer(serializers.ModelSerializer):
    class Meta:
            model = earthquake_bulletins
            fields = ('rbtype_id','bulletin_no','_precise_id','_time_sec','_body','_eqinfo_json','_precise_info',
                '_sealvl_info','_inun_id','_precise_eqref','event_id','_in_scs')
            extra_kwargs = {
                '_precise_info': {
                    'required': False,
                    'allow_blank': True,
                },
                '_sealvl_info': {
                    'required': False,
                    'allow_blank': True,
                },
                '_inun_id': {
                    'required': False,
                    'allow_blank': True,
                },
                '_usgs_shakecast_url': {
                    'required': False,
                    'allow_blank': True,
                }
            }