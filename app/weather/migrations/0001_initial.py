# Generated by Django 4.0.2 on 2022-03-28 09:31

from django.db import migrations, models
import django.db.models.deletion


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
                ('country_name', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'country',
            },
        ),
        migrations.CreateModel(
            name='province',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('province_id', models.CharField(max_length=10)),
                ('province_name', models.CharField(max_length=128)),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.country')),
            ],
            options={
                'db_table': 'province',
            },
        ),
        migrations.CreateModel(
            name='observation_metdata',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('station_name', models.CharField(max_length=128)),
                ('date', models.DateField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('rainfall', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_T', models.DecimalField(decimal_places=2, max_digits=10)),
                ('min_T', models.DecimalField(decimal_places=2, max_digits=10)),
                ('country_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.country')),
            ],
            options={
                'db_table': 'observation_metdata',
            },
        ),
        migrations.CreateModel(
            name='district',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('province_name', models.CharField(max_length=128)),
                ('district_id', models.CharField(max_length=10)),
                ('district_name', models.CharField(max_length=128)),
                ('province_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.province')),
            ],
            options={
                'db_table': 'district',
            },
        ),
        migrations.CreateModel(
            name='commune',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('district_name', models.CharField(max_length=128)),
                ('commune_id', models.CharField(max_length=10)),
                ('commune_name', models.CharField(max_length=10)),
                ('district_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.district')),
            ],
            options={
                'db_table': 'commune',
            },
        ),
    ]
