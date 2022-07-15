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
    ################################ Hazard Module ##############################################
    path('hazard_analytics', da_views.hazard_ana, name='hazard_ana'),
    path('hazard_analytics/hazard_cambodia', da_views.hazard_cambodia, name='hazard_ana_cambodia'), # AJAX in hazard_analytics page
    path('hazard_analytics/hazard_cambodia_yearselected', da_views.hazard_cambodia_yearselected, name='hazard_ana_cambodia_yearselected'),

    path('hazard_analytics/hazard_laos', da_views.hazard_laos, name='hazard_ana_laos'), # AJAX in hazard_analytics page
    path('hazard_analytics/hazard_laos_yearselected', da_views.hazard_laos_yearselected, name='hazard_ana_laos_yearselected'),
    ################################ Disaster Module ##############################################
    path('disaster_analytics', da_views.disaster_ana, name='disaster_ana'), 
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
    ##############################################################################
    path('upload_data', wf_views.upload_data, name='upload_data'),
    path('sdc_project', wf_views.sdc_project, name='sdc_project'),
    path('reports', wf_views.reports, name='reports'),
  

]
     