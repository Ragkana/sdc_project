# Generated by Django 4.0.2 on 2022-10-07 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='disaster',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('province_id', models.CharField(max_length=10)),
                ('province_name', models.CharField(max_length=128)),
                ('district_id', models.CharField(max_length=10)),
                ('district_name', models.CharField(max_length=128)),
                ('commune_id', models.CharField(max_length=10)),
                ('commune_name', models.CharField(max_length=128)),
                ('date_data', models.DateField()),
                ('event', models.CharField(max_length=128)),
                ('datacard_records', models.IntegerField()),
                ('deaths', models.IntegerField()),
                ('injured', models.IntegerField()),
                ('missing', models.IntegerField()),
                ('house_destroy', models.IntegerField()),
                ('house_damage', models.IntegerField()),
                ('directly_affected', models.IntegerField()),
                ('indirectly_affected', models.IntegerField()),
                ('relocated', models.IntegerField()),
                ('evacuated', models.IntegerField()),
                ('losses_usd', models.DecimalField(decimal_places=2, max_digits=10)),
                ('losses_local', models.DecimalField(decimal_places=2, max_digits=10)),
                ('education_centers', models.IntegerField()),
                ('hospitals', models.IntegerField()),
                ('damages_crops_ha', models.DecimalField(decimal_places=2, max_digits=10)),
                ('other_sector', models.CharField(max_length=128)),
                ('glide_number', models.CharField(max_length=128)),
                ('comment', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'disaster',
            },
        ),
        migrations.CreateModel(
            name='sdc_project_location_cambodia',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('project', models.CharField(max_length=256)),
                ('country_id', models.CharField(max_length=10)),
                ('country_name', models.CharField(max_length=128)),
                ('province_id', models.CharField(max_length=10)),
                ('province_name', models.CharField(max_length=128)),
                ('district_id', models.CharField(max_length=10)),
                ('district_name', models.CharField(max_length=128)),
                ('commune_id', models.CharField(max_length=10)),
                ('commune_name', models.CharField(max_length=128)),
                ('latitude', models.DecimalField(decimal_places=11, max_digits=18)),
                ('longitude', models.DecimalField(decimal_places=11, max_digits=18)),
                ('detail', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'sdc_project_location_cambodia',
            },
        ),
        migrations.CreateModel(
            name='sdc_project_location_laos',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('project', models.CharField(max_length=256)),
                ('country_id', models.CharField(max_length=10)),
                ('country_name', models.CharField(max_length=128)),
                ('province_id', models.CharField(max_length=10)),
                ('province_name', models.CharField(max_length=128)),
                ('district_id', models.CharField(max_length=10)),
                ('district_name', models.CharField(max_length=128)),
                ('commune_id', models.CharField(max_length=10)),
                ('commune_name', models.CharField(max_length=128)),
                ('latitude', models.DecimalField(decimal_places=11, max_digits=18)),
                ('longitude', models.DecimalField(decimal_places=11, max_digits=18)),
                ('detail', models.CharField(max_length=512)),
            ],
            options={
                'db_table': 'sdc_project_location_laos',
            },
        ),
        migrations.CreateModel(
            name='vulnerability_mpi',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('country_id', models.CharField(max_length=10)),
                ('province_id', models.CharField(max_length=10)),
                ('province_name', models.CharField(max_length=128)),
                ('mpi', models.DecimalField(decimal_places=5, max_digits=100)),
                ('population_in_mpi', models.DecimalField(decimal_places=5, max_digits=100)),
                ('intensity_of_deprivation', models.DecimalField(decimal_places=5, max_digits=100)),
                ('vulnerable_to_poverty', models.DecimalField(decimal_places=5, max_digits=100)),
                ('in_severe_poverty', models.DecimalField(decimal_places=5, max_digits=100)),
                ('population_share', models.DecimalField(decimal_places=5, max_digits=100)),
                ('population_size', models.DecimalField(decimal_places=5, max_digits=100)),
                ('number_of_mpi', models.DecimalField(decimal_places=5, max_digits=100)),
            ],
            options={
                'db_table': 'vulnerability_mpi',
            },
        ),
    ]
