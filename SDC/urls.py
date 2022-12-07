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
from django.urls import path, include

from django.contrib.auth import views as auth

from app.weather import views as wf_views
from app.earthquake import views as eq_views
from app.disaster_ana import views as da_views
from app.report_n_project import views as rp_views
from app.api import views as api_views
from app.sdc_auth import views as auth_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.dashboard, name= 'dashboard'), #Work with Homepage
    ################################ Login Module ##############################################
    ## Login & Log out ##
    path('', auth_view.login_sdc, name='login'),
    path('logout', auth.LogoutView.as_view(template_name ='login.html'), name='logout'),

    ## Register ##
    path('register', auth_view.register, name='register'),
    path('register_success', auth_view.register_success, name='register_success'),

    ## Forget password ##
    path('reset_password/', auth.PasswordResetView.as_view(template_name="login_sys/password_reset.html"), name="reset_password"),
    path('reset_password/sent', auth.PasswordResetDoneView.as_view(template_name="login_sys/password_reset_done.html"), name="password_reset_done"),
    path('reset_password/<uidb64>/<token>', auth.PasswordResetConfirmView.as_view(template_name="login_sys/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password/complete', auth.PasswordResetCompleteView.as_view(template_name="login_sys/password_reset_complete.html"), name="password_reset_complete"),

    ################################ Weather Forecast Module ##############################################
    path('weather_forecast', wf_views.weather_forecast_mod, name='weather_forecast'),
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
    path('hazard_analytics/hazard_khm_csv', da_views.hazard_khm_csv, name='hazard_cambodia_csv'),

    path('hazard_analytics/hazard_laos', da_views.hazard_laos, name='hazard_ana_laos'), # AJAX in hazard_analytics page
    path('hazard_analytics/hazard_laos_yearselected', da_views.hazard_laos_yearselected, name='hazard_ana_laos_yearselected'),
    path('hazard_analytics/hazard_laos_csv', da_views.hazard_lao_csv, name='hazard_laos_csv'),
    ################################ Disaster Module ##############################################
    path('disaster_analytics', da_views.disaster_ana, name='disaster_ana'), 

    path('disaster_analytics/cambodia', da_views.disaster_ana_khm, name='disaster_ana_cambodia'), 
    path('disaster_analytics/cambodia_yearsel', da_views.disaster_ana_khm_yearsel, name='disaster_ana_cambodia_yearsel'), 

    path('disaster_analytics/laos', da_views.disaster_ana_lao, name='disaster_ana_laos'),
    path('disaster_analytics/laos_yearsel', da_views.disaster_ana_lao_yearsel, name='disaster_ana_laos_yearsel'),

    path('disaster_analytics/myanmar', da_views.disaster_ana_mya, name='disaster_ana_myanmar'),
    path('disaster_analytics/myanmar_yearsel', da_views.disaster_ana_mya_yearsel, name='disaster_ana_myanmar_yearsel'),
    ################################ Vulnerability Module ##############################################
    path('vulnerability', da_views.vulnerability, name='vulnerability'),

    path('vulnerability/cambodia_population', da_views.vul_khm_population, name='vulnerability_cambodia_population'),
    path('vulnerability/cambodia_mpi', da_views.vul_khm_mpi, name='vulnerability_cambodia_mpi'),
    path('vulnerability/khm_population_csv', da_views.population_khm_csv, name='khm_population_csv'),
    path('vulnerability/khm_mpi_csv', da_views.mpi_khm_csv, name='khm_mpi_csv'),

    path('vulnerability/laos_population', da_views.vul_lao_population, name='vulnerability_laos_population'),
    path('vulnerability/laos_mpi', da_views.vul_lao_mpi, name='vulnerability_laos_mpi'),
    path('vulnerability/lao_population_csv', da_views.population_lao_csv, name='lao_population_csv'),
    path('vulnerability/lao_mpi_csv', da_views.mpi_lao_csv, name='lao_mpi_csv'),
    ################################ Earthquake Module ##############################################
    path('earthquake', eq_views.earthquake, name='earthquake'),
    path('earthquake/setting', eq_views.setting, name='earthquake-setting'),
    path('earthquake/send_advisory', eq_views.send_advisory, name='earthquake-send-advisory'),
    path('earthquake/view-bulletin/<str:event_id>/<int:bulletin_no>/', eq_views.view_bulletin, name='earthquake-view-bulletin'),
    path('earthquake/import', api_views.import_earthquake, name='import-earthquake'),
    path('earthquake/import/bulletin', api_views.import_bulletin, name='import-earthquake'),
    path('earthquake/filter-earthquake', eq_views.filter_earthquake, name='filter-earthquake'),
    ################################# Upload Data #############################################
    path('upload_data', rp_views.upload_data, name='upload_data'),
    path('upload_data/country_choose', rp_views.country_choose, name='upload_data_country'),
    path('upload_data/province_choose', rp_views.province_choose, name='upload_data_province'),
    path('upload_data/district_choose', rp_views.district_choose, name='upload_data_district'),
    ################################# SDC Project #############################################
    path('sdc_project_cambodia', rp_views.sdc_project_khm, name='sdc_project_cambodia'),
    path('sdc_project_laos', rp_views.sdc_project_lao, name='sdc_project_laos'),
    path('sdc_project_myanmar', rp_views.sdc_project_mya, name='sdc_project_myanmar'),

    path('sdc_project_location', rp_views.sdc_project_location, name='sdc_project_location'),
    path('sdc_project_location/country_project_choose', rp_views.country_project_choose, name='sdc_project_country'),
    ################################# Reports And Project #############################################
    path('reports', rp_views.reports, name='reports'),
    path('upload_data/country_event', rp_views.country_event, name='report_country'),
    path('reports/reports_pdf', rp_views.report_pdf, name='reports_pdf'),
    ################################# About US Project #############################################
    path('about_sdc', rp_views.about_sdc, name='about_sdc'),
  
]
     