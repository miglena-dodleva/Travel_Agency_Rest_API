from django.db import models

# Create your models here.


class Location(models.Model):
    street = models.CharField(max_length=200)
    number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    #imageURL = models.URLField()

    def __str__(self):
        return self.street + ' ' + self.number + ' ' + self.city + ' ' + self.country


class Holiday(models.Model):
    title = models.CharField(max_length=200)
    startDate = models.CharField(max_length=50)
    duration = models.IntegerField()
    price = models.FloatField()
    freeSlots = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)


class Reservation(models.Model):
    contactName = models.CharField(max_length=200)
    phoneNumber = models.CharField(max_length=20)
    holiday = models.ForeignKey(Holiday, on_delete=models.CASCADE)
