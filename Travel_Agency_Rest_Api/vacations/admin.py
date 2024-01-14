from django.contrib import admin

from vacations.models import Location, Reservation, Holiday

# Register your models here

admin.site.register(Location)
admin.site.register(Holiday)
admin.site.register(Reservation)
