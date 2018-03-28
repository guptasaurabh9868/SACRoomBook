# - * - coding: utf-8 - * - 
from  django.conf.urls  import  include, url 
from  django.views.generic  import TemplateView
from booking import views

urlpatterns  = [
    url(r'^booking/',views.booking, name='booking'),
    url(r'^not_approved_yet/',views.not_approved, name='not_approved'),
    url(r'^my_bookings/',views.display_requests, name='my_bookings'),
    url(r'^delete/(?P<id>\d+)/', views.delete_request, name='delete_request'),
    url(r'^approved/(?P<id>\d+)/',views.approved, name='approved'),
    url(r'rejected/(?P<id>\d+)/', views.rejected, name='rejected'),
]