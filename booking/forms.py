from django import forms
from booking import models

class BookingForm(forms.ModelForm):

    class Meta:
        model = models.Booking
        fields = ('Room_no', 'Booking_start', 'Booking_end', )