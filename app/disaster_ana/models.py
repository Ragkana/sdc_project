from django.db import models

# Create your models here.
# Retrieve data from province table
class disaster(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    province_id = models.CharField(max_length=10, null=False)
    province_name = models.CharField(max_length=128)
    district_id = models.CharField(max_length=10)
    district_name = models.CharField(max_length=128)
    commune_id = models.CharField(max_length=10)
    commune_name = models.CharField(max_length=128)
    date_data = models.DateField()
    event = models.CharField(max_length=128)
    datacard_records = models.IntegerField()
    deaths = models.IntegerField()
    injured = models.IntegerField()
    missing = models.IntegerField()
    house_destroy = models.IntegerField()
    house_damage = models.IntegerField()
    directly_affected = models.IntegerField()
    indirectly_affected = models.IntegerField()
    relocated = models.IntegerField()
    evacuated = models.IntegerField()
    losses_usd = models.DecimalField(max_digits=10, decimal_places=2)
    losses_local = models.DecimalField(max_digits=10, decimal_places=2)
    education_centers = models.IntegerField()
    hospitals = models.IntegerField()
    damages_crops_ha = models.DecimalField(max_digits=10, decimal_places=2)
    other_sector = models.CharField(max_length=128)
    glide_number = models.CharField(max_length=128)
    class Meta:
        db_table = "disaster"

