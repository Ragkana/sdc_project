# Generated by Django 4.0.2 on 2022-11-07 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='country',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('country_id', models.CharField(max_length=10)),
                ('country_name', models.CharField(max_length=128)),
                ('province_id', models.CharField(max_length=10)),
                ('province_name', models.CharField(max_length=128)),
                ('district_id', models.CharField(max_length=10)),
                ('district_name', models.CharField(max_length=128)),
                ('commune_id', models.CharField(max_length=10)),
                ('commune_name', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='sdc_project_cambodia',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('project_fullname', models.CharField(max_length=256)),
                ('project_shortname', models.CharField(max_length=128)),
                ('objective', models.CharField(max_length=512)),
                ('duration', models.CharField(max_length=256)),
                ('budget', models.CharField(max_length=256)),
                ('location', models.CharField(max_length=256)),
                ('partners', models.CharField(max_length=256)),
                ('outcome', models.CharField(max_length=512)),
                ('pdf_download', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'sdc_project_cambodia',
            },
        ),
        migrations.CreateModel(
            name='sdc_project_laos',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('project_fullname', models.CharField(max_length=256)),
                ('project_shortname', models.CharField(max_length=128)),
                ('objective', models.CharField(max_length=512)),
                ('duration', models.CharField(max_length=256)),
                ('budget', models.CharField(max_length=256)),
                ('location', models.CharField(max_length=256)),
                ('partners', models.CharField(max_length=256)),
                ('outcome', models.CharField(max_length=512)),
                ('pdf_download', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'sdc_project_laos',
            },
        ),
    ]
