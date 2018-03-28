from django.contrib.auth.models import User
from django.db import models

from main.models import Profile


# Create your models here.
class Room(models.Model):
    Room_no = models.CharField(max_length=10)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Booking(models.Model):
    Room_no = models.ForeignKey(Room, on_delete=models.CASCADE)
    Booking_start  = models.DateTimeField()
    Booking_end = models.DateTimeField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)  
    Approved = models.BooleanField(default=False)
    Rejected = models.BooleanField(default=False)

    class Meta:
        ordering = ['Booking_start']


    def __str__(self):
        return "%s is to be Booked from %s to %s " %(self.Room_no, self.Booking_start , self.Booking_end)