# Generated by Django 4.0.2 on 2022-03-29 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_alter_observation_metdata_country_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation_metdata',
            name='country_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weather.country'),
        ),
    ]
