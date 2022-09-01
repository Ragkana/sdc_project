from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
# For log in
from django.contrib.auth import authenticate, logout, login
# import Django database for User
from django.contrib.auth.models import User
# For forget password: mail exist chack


import json

## Email Library ##
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.
#########################################################################
############################# Log in Module #############################
#########################################################################
def login_sdc(request):
    error_m = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            # Log a user in
            login(request, user)
            return redirect("weather_forecast")
        else:
            error_m = "Username/Password is invalid."
            return render(request, "login_sys/login.html", {'error':error_m})
    return render(request, "login_sys/login.html")

    
###########################################################################
########################### Registration Module ###########################
########################################################################### 
def register(request):
    ## Send all mail data ##
    all_mail = list(User.objects.values_list('email', flat=True))
    all_mail = json.dumps(all_mail)

    first_name, last_name, email, c_password = "", "", "", ""
    if request.method == 'POST':
        first_name = request.POST.get('f_name')
        last_name = request.POST.get('l_name')
        email = request.POST.get('email')
        c_password = request.POST.get('password02')
        user = User.objects.create_user(username=email, email=email, first_name=first_name, last_name=last_name, password=c_password)
        user.save()
        ## Send email verification for successful registration ##
        subject = 'welcome to SDC Portal'
        message = f'Hi {user.first_name} {user.last_name}, thank you for registering in SDC Portal.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail( subject, message, email_from, recipient_list )

        return redirect("register_success")

    return render(request, "login_sys/register.html",{'all_mail':all_mail})

def register_success(request):
    return render(request, "login_sys/register_success.html")


##############################################################################
########################### Forgot Password Module ###########################
##############################################################################

