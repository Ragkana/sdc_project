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
from app.weather import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.dashboard, name= 'dashboard'), #Work with Homepage
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('', views.weather_forecast, name='weather_forecast'),
    path('observation', views.observation, name='observation'),
    path('hazard_analytics', views.hazard_ana, name='hazard_ana'),
    path('disaster_analytics', views.disaster_ana, name='disaster_ana'),
    path('earthquake', views.earthquake, name='earthquake'),
    path('share_data', views.share_data, name='share_data'),
    path('sdc_project', views.sdc_project, name='sdc_project'),
    path('reports', views.reports, name='reports'),
]
     