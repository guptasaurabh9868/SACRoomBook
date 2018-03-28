from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.template.loader import render_to_string

from datetime import datetime
import dateutil.parser 
import pytz

from booking.forms import BookingForm
from booking.models import *
# Create your views here.


def booking(request):
    form = BookingForm()
    wrong_date_selection = False
    clash = False
    request_made = False
    if request.POST:
        form = BookingForm(request.POST)
        utc = pytz.UTC
        room_no = request.POST['Room_no']
        booking_start = utc.localize(dateutil.parser.parse(request.POST['Booking_start']))
        booking_end = utc.localize(dateutil.parser.parse(request.POST['Booking_end']))

        print(room_no, booking_start, booking_end)
        
        if booking_start > booking_end :
            wrong_date_selection = True
            print("Wrong Date Selected.")
            return render(request,'booking.html',{'verified':request.user.profile.email_confirmed, 'wrong_date_selection':wrong_date_selection, 'form' : form })
        else:
            for booking in Booking.objects.filter(Room_no=room_no):
                if (booking_start >= booking.Booking_start and booking_start <= booking.Booking_end ) or ( booking_end >= booking.Booking_start and booking_end <= booking.Booking_end ) or(booking_start < booking.Booking_start and booking_end > booking.Booking_end):
                    clash = True
                    return render(request,'booking.html',{'verified':request.user.profile.email_confirmed, 'booking':booking, 'clash': clash, 'form' : form })

            booking  = Booking(Room_no=Room.objects.get(pk=room_no), Booking_start=booking_start, Booking_end=booking_end, user=request.user.profile)
            booking.save()
            request_made = True
            return render(request,'booking.html',{'verified':request.user.profile.email_confirmed,'booking':booking, 'form' : form, 'request_made':request_made })
    else:
        print("Inside Booking")        
        return render(request,'booking.html',{'verified':request.user.profile.email_confirmed,'form' : form, 'clash': clash, 'wrong_date_selection':wrong_date_selection})

def approved(request):
    return render(request,'approved.html')

def not_approved(request):
    return render(request,'not_approved.html')

def display_requests(request):
    if request.user.is_staff:
        my_bookings = Booking.objects.all()
    else:
        my_bookings = Booking.objects.filter(user=request.user.profile)
    return render(request,'display_my_bookings.html',{'my_bookings':my_bookings, 'verified':request.user.profile.email_confirmed})

def delete_request(request, id):
    booking = Booking.objects.get(id=id)
    if request.user.is_staff:
        from_mail = settings.EMAIL_HOST_USER
        to_list = [ booking.user.email ]
        subject = "Your Booking is Deleted."
        message = render_to_string('booking_deleted.html', {
                    'user': booking.user,
                })
        print(from_mail, to_list, subject, message)
        send_mail(subject,message, from_mail, to_list, fail_silently=True)
    booking.delete()
    return HttpResponseRedirect('/my_bookings/')

def approved(request, id):
    booking = Booking.objects.get(id=id)
    booking.Approved = True
    booking.Rejected = False
    booking.save()
    return HttpResponseRedirect('/my_bookings/')

def rejected(request, id):
    booking = Booking.objects.get(id=id)
    booking.Rejected = True
    booking.Approved = False
    booking.save()
    return HttpResponseRedirect('/my_bookings/')