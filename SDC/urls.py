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
from app.disaster_ana import views as da_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.dashboard, name= 'dashboard'), #Work with Homepage
    path('login', wf_views.login, name='login'),
    path('register', wf_views.register, name='register'),
    path('forgot_password', wf_views.forgot_password, name='forgot_password'),
    path('', wf_views.weather_forecast_mod, name='weather_forecast'),
    path('observation', wf_views.observation, name='observation'),
    path('hazard_analytics', da_views.hazard_ana, name='hazard_ana'),
    path('disaster_analytics', da_views.disaster_ana, name='disaster_ana'),
    path('earthquake', wf_views.earthquake, name='earthquake'),
    path('share_data', wf_views.share_data, name='share_data'),
    path('sdc_project', wf_views.sdc_project, name='sdc_project'),
    path('reports', wf_views.reports, name='reports'),
]
     