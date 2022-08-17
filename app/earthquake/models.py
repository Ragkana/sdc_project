from django.db import models

# Create your models here.
# Retrieve data from earthquake_events table
class earthquake_events(models.Model):
    event_id        = models.CharField(primary_key=True, max_length=50, null=False)
    latitude        = models.DecimalField(decimal_places=2,max_digits=10, null=False)
    longitude       = models.DecimalField(decimal_places=2,max_digits=10, null=False)
    magnitude       = models.DecimalField(decimal_places=2,max_digits=4, null=False)
    phase_count     = models.PositiveSmallIntegerField(null=False,default=0)
    mag_type        = models.CharField(max_length=10, null=False)
    depth           = models.CharField(max_length=10, null=False)
    event_datetime  = models.DateTimeField()
    region          = models.CharField(max_length=150, null=False)
    bulletin_no     = models.PositiveSmallIntegerField( null=True, default=0)
    status          = models.CharField(max_length=2, null=True, default='N')
    is_fake         = models.BooleanField( null=True, default=False)
    is_inside       = models.BooleanField( null=True, default=False)
    source          = models.CharField(max_length=10, null=True,default='RIMES')
    create_date     = models.DateTimeField( null=True,auto_now_add=True)
    update_date     = models.DateTimeField( null=True,auto_now=True)
    class Meta:
        db_table = "earthquake_events"

class earthquake_bulletins(models.Model):
    id              = models.AutoField(primary_key=True)
    event_id        = models.CharField(max_length=50, null=True)
    rbtype_id       = models.IntegerField(default=0, null=True)
    bulletin_no     = models.IntegerField(default=0, null=True)
    _precise_id     = models.IntegerField(default=0, null=True)
    _time_sec       = models.IntegerField(default=0, null=True)
    _body           = models.TextField(null=True, default='')
    _eqinfo_json    = models.TextField(null=True, default='')
    _precise_info   = models.TextField(null=True, default='')
    _sealvl_info    = models.TextField(null=True, default='')
    _inun_id        = models.TextField(null=True, default='')
    _in_scs         = models.IntegerField(default=0, null=True)
    _precise_eqref  = models.IntegerField(default=0, null=True)
    _usgs_shakecast_url    = models.TextField(null=True, default='')
    class Meta:
        db_table = "earthquake_bulletins"

# Retrieve data from earthquake_events table
class earthquake_settings(models.Model):
    id              = models.CharField(primary_key=True, max_length=11, null=False)
    simulation      = models.BooleanField(default=0)
    number_events   = models.PositiveSmallIntegerField(null=False)
    auto_send       = models.BooleanField(default=0)
    auto_send_email = models.TextField(null=True, default='')
    filter_1        = models.BooleanField(default=0) # For magnitude < 5.0
    filter_2        = models.BooleanField(default=0) # For magnitude < 5.0
    filter_3        = models.BooleanField(default=0) # For magnitude < 5.0
    filter_4        = models.BooleanField(default=0) # For magnitude < 5.0
    inside_aoi      = models.BooleanField(default=0) # For magnitude < 5.0
    show_aor        = models.BooleanField(default=0)
    show_aoi        = models.BooleanField(default=0)
    show_heatmap    = models.BooleanField(default=0)
    points1         = models.TextField(null=True, default='')
    points2         = models.TextField(null=True, default='')
    points3         = models.TextField(null=True, default='')
    class Meta:
        db_table = "earthquake_settings"
