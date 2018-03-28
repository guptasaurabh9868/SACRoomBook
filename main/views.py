from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
# from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from datetime import datetime
import dateutil.parser 
import pytz

from booking.forms import BookingForm
from main.forms import SignUpForm
from main.tokens import account_verification_token
from main.models import *


@login_required
def home(request):
    # login(request, user)
    return render(request, 'home.html')


def login_user(request):
    login_failed = False
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login_failed = False
            form = BookingForm()
            if user.is_active:
                login(request, user)
                print("User is Not none and active as well.")
            else:
                login(request, user)
                print("User is Not None but not Active.")

            return HttpResponseRedirect('/booking/',{'verified':request.user.profile.email_confirmed, 'login_failed':login_failed, 'form' : form })
        else:
            login_failed = True
            print("User is None")
    return render(request,'home.html',{ 'login_failed':login_failed })

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def registration(request):
    logout(request)
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.is_active = True
            user.save()

            from_mail = settings.EMAIL_HOST_USER
            to_list = ['guptasaurabh9868@gmail.com', settings.EMAIL_HOST_USER ]

            current_site = get_current_site(request)
            subject = 'Approve '+ user.username +' SACRoom Booking Account'
            message = render_to_string('account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_verification_token.make_token(user),
            })
            login(request, user)
            send_mail(subject,message, from_mail, to_list, fail_silently=True)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
        print("Here")
    return render(request, 'registration.html', {'form': form})

def account_activation_sent(request):
    if request.user.is_authenticated:
        return render(request, 'account_activation_sent.html')
    else:
        return redirect('home')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_verification_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        from_mail = settings.EMAIL_HOST_USER
        to_list = [user.email]
        subject = 'SAC Room Booking Account Verified.'
        message = render_to_string('account_verified_email.html', {
                'user': user,
            })
        send_mail(subject,message, from_mail, to_list, fail_silently=True)
        return redirect('account_verified')
    else:
        return render(request, 'account_activation_invalid.html')

def account_verified(request):
    return render(request,'account_verified.html')


