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
        
        if (booking_start > booking_end) or (booking_start < utc.localize(datetime.now()) or booking_end < utc.localize(datetime.now())):
            wrong_date_selection = True
            print("Wrong Date Selected.")
            return render(request,'booking.html',{'verified':request.user.profile.email_confirmed, 'wrong_date_selection':wrong_date_selection, 'form' : form })
        else:
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
        to_list = [ booking.user.user.email ]
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
    all_bookings = Booking.objects.all()
    for book in Booking.objects.filter(Room_no=booking.Room_no,Approved=True).exclude():
        if (booking.Booking_start >= book.Booking_start and booking.Booking_start <= book.Booking_end ) or ( booking.Booking_end >= book.Booking_start and booking.Booking_end <= book.Booking_end ) or(booking.Booking_start < book.Booking_start and booking.Booking_end > book.Booking_end):
            if booking.id == book.id:
                continue
            clash = True
            return render(request,'display_all_bookings.html',{'verified':request.user.profile.email_confirmed, 'clash_booking':booking, 'clash': clash, 'all_bookings' : all_bookings })
    booking.Approved = True
    booking.Rejected = False
    if request.user.is_staff:
        from_mail = settings.EMAIL_HOST_USER
        to_list = [ booking.user.user.email ]
        subject = "Your Booking is Approved."
        message = render_to_string('booking_approved.html', {
                    'user': booking.user,
                })
        print(from_mail, to_list, subject, message)
        send_mail(subject,message, from_mail, to_list, fail_silently=True)
    booking.save()
    return HttpResponseRedirect('/my_bookings/')

def rejected(request, id):
    booking = Booking.objects.get(id=id)
    booking.Rejected = True
    booking.Approved = False
    if request.user.is_staff:
        from_mail = settings.EMAIL_HOST_USER
        to_list = [ booking.user.user.email ]
        subject = "Your Booking is Rejected."
        message = render_to_string('booking_rejected.html', {
                    'user': booking.user,
                })
        print(from_mail, to_list, subject, message)
        send_mail(subject,message, from_mail, to_list, fail_silently=True)
    booking.save()
    return HttpResponseRedirect('/my_bookings/')

def display_all_requests(request):
    if request.user.is_staff:
        all_bookings = Booking.objects.all()
    else:
        all_bookings = Booking.objects.filter(Approved=True)
    return render(request,'display_all_bookings.html',{'all_bookings':all_bookings, 'verified':request.user.profile.email_confirmed})
