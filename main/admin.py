from django.contrib import admin

# Register your models here.
from main import models as mm
from booking import models as bm
admin.site.register(mm.Profile)
admin.site.register(bm.Room)
admin.site.register(bm.Booking)