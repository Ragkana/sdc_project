from django.shortcuts import render
from app.weather import views

# Create your views here.
def hazard_ana(request):
    return render(request, "hazard_ana.html", {'url_name': 'hazard_ana'})

def disaster_ana(request):
    return render(request, "disaster_ana.html", {'url_name': 'disaster_ana'})