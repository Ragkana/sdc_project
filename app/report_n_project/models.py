from django.db import models

# Create your models here.
class country(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    country_id = models.CharField(max_length=10)
    country_name = models.CharField(max_length=128)
    province_id = models.CharField(max_length=10)
    province_name = models.CharField(max_length=128)
    district_id = models.CharField(max_length=10)
    district_name = models.CharField(max_length=128)
    commune_id = models.CharField(max_length=10)
    commune_name = models.CharField(max_length=128)
    class Meta:
        db_table = 'country'

class sdc_project_cambodia(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    project_fullname = models.CharField(max_length=256, null=False)
    project_shortname = models.CharField(max_length=128, null=False)
    objective = models.CharField(max_length=512)
    duration = models.CharField(max_length=256)
    budget = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    partners = models.CharField(max_length=256)
    outcome = models.CharField(max_length=512)
    pdf_download = models.CharField(max_length=256)
    class Meta:
        db_table = "sdc_project_cambodia"

class sdc_project_laos(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    project_fullname = models.CharField(max_length=256, null=False)
    project_shortname = models.CharField(max_length=128, null=False)
    objective = models.CharField(max_length=512)
    duration = models.CharField(max_length=256)
    budget = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    partners = models.CharField(max_length=256)
    outcome = models.CharField(max_length=512)
    pdf_download = models.CharField(max_length=256)
    class Meta:
        db_table = "sdc_project_laos"

class sdc_project_myanmar(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    project_fullname = models.CharField(max_length=256, null=False)
    project_shortname = models.CharField(max_length=128, null=False)
    objective = models.CharField(max_length=512)
    duration = models.CharField(max_length=256)
    budget = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    partners = models.CharField(max_length=256)
    outcome = models.CharField(max_length=512)
    pdf_download = models.CharField(max_length=256)
    class Meta:
        db_table = "sdc_project_myanmar"

class reports_temporary(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    country_id = models.CharField(max_length=10)
    hazard_type = models.CharField(max_length=50)
    hazard_p = models.IntegerField()
    disaster_p = models.IntegerField()
    vulnerability_p = models.IntegerField()
    class Meta:
        db_table = "reports_temporary"

