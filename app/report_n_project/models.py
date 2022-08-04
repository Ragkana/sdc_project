from django.db import models

# Create your models here.
class sdc_project_cambodia(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    project_name = models.CharField(max_length=256, null=False)
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
    project_name = models.CharField(max_length=256, null=False)
    objective = models.CharField(max_length=512)
    duration = models.CharField(max_length=256)
    budget = models.CharField(max_length=256)
    location = models.CharField(max_length=256)
    partners = models.CharField(max_length=256)
    outcome = models.CharField(max_length=512)
    pdf_download = models.CharField(max_length=256)
    class Meta:
        db_table = "sdc_project_laos"

