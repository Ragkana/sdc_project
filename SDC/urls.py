"""SDC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.weather import views as wf_views
from app.earthquake import views as eq_views
from app.disaster_ana import views as da_views
from app.report_n_project import views as rp_views
from app.api import views as api_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.dashboard, name= 'dashboard'), #Work with Homepage
    path('login', wf_views.login, name='login'),
    path('register', wf_views.register, name='register'),
    path('forgot_password', wf_views.forgot_password, name='forgot_password'),
    ################################ Weather Forecast Module ##############################################
    path('', wf_views.weather_forecast_mod, name='weather_forecast'),
    path('weather_cambodia', wf_views.wf_cambodia_submit, name='wf_cambodia_submit'),
    path('weather_laos', wf_views.wf_laos_submit, name='wf_laos_submit'),
    ################################ Observation Module ##############################################
    path('observation', wf_views.observation, name='observation'),

    path('observation/cambodia_station', wf_views.obs_khm_station, name='obs_cambodia_station'),
    path('observation/cambodia_station_yearsel', wf_views.obs_khm_station_yearsel, name='obs_cambodia_station_yearsel'),

    path('observation/laos_station', wf_views.obs_lao_station, name='obs_laos_station'),
    path('observation/laos_station_yearsel', wf_views.obs_lao_station_yearsel, name='obs_laos_station_yearsel'),
    ################################ Hazard Module ##############################################
    path('hazard_analytics', da_views.hazard_ana, name='hazard_ana'),
    path('hazard_analytics/hazard_cambodia', da_views.hazard_cambodia, name='hazard_ana_cambodia'), # AJAX in hazard_analytics page
    path('hazard_analytics/hazard_cambodia_yearselected', da_views.hazard_cambodia_yearselected, name='hazard_ana_cambodia_yearselected'),

    path('hazard_analytics/hazard_laos', da_views.hazard_laos, name='hazard_ana_laos'), # AJAX in hazard_analytics page
    path('hazard_analytics/hazard_laos_yearselected', da_views.hazard_laos_yearselected, name='hazard_ana_laos_yearselected'),
    ################################ Disaster Module ##############################################
    path('disaster_analytics', da_views.disaster_ana, name='disaster_ana'), 

    path('disaster_analytics/cambodia', da_views.disaster_ana_khm, name='disaster_ana_cambodia'), 
    path('disaster_analytics/cambodia_yearsel', da_views.disaster_ana_khm_yearsel, name='disaster_ana_cambodia_yearsel'), 

    path('disaster_analytics/laos', da_views.disaster_ana_lao, name='disaster_ana_laos'),
    path('disaster_analytics/laos_yearsel', da_views.disaster_ana_lao_yearsel, name='disaster_ana_laos_yearsel'),
    ################################ Vulnerability Module ##############################################
    path('vulnerability', da_views.vulnerability, name='vulnerability'),

    path('vulnerability/cambodia_population', da_views.vul_khm_population, name='vulnerability_cambodia_population'),
    path('vulnerability/cambodia_mpi', da_views.vul_khm_mpi, name='vulnerability_cambodia_mpi'),

    path('vulnerability/laos_population', da_views.vul_lao_population, name='vulnerability_laos_population'),
    path('vulnerability/laos_mpi', da_views.vul_lao_mpi, name='vulnerability_laos_mpi'),
    ################################ Earthquake Module ##############################################
    path('earthquake', eq_views.earthquake, name='earthquake'),
    path('earthquake/setting', eq_views.setting, name='earthquake-setting'),
    path('earthquake/send_advisory', eq_views.send_advisory, name='earthquake-send-advisory'),
    path('earthquake/view-bulletin/<str:event_id>/<int:bulletin_no>/', eq_views.view_bulletin, name='earthquake-view-bulletin'),
    path('earthquake/import', api_views.import_earthquake, name='import-earthquake'),
    path('earthquake/import/bulletin', api_views.import_bulletin, name='import-earthquake'),
    ################################# Upload Data #############################################
    path('upload_data', rp_views.upload_data, name='upload_data'),
    path('upload_data/country_choose', rp_views.country_choose, name='upload_data_country'),
    ################################# SDC Project #############################################
    path('sdc_project', rp_views.sdc_project, name='sdc_project'),
    path('sdc_project_cambodia', rp_views.sdc_project_khm, name='sdc_project_cambodia'),
    path('sdc_project_laos', rp_views.sdc_project_lao, name='sdc_project_laos'),
    path('sdc_project_myanmar', rp_views.sdc_project_mya, name='sdc_project_myanmar'),
    path('sdc_project/add_cambodia', rp_views.khm_add_project, name='sdc_project_add_cambodia'),
    ################################# Reports And Project #############################################
    path('reports', rp_views.reports, name='reports'),
    path('reports/reports_pdf', rp_views.report_pdf, name='reports_pdf'),
  
]
     