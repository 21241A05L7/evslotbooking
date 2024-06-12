from django.db import models
import uuid


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.email

class EVStation(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
    
class EV(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=100)

    def __str__(self):
        return self.number

class Slot(models.Model):
    ev_station_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    email = models.EmailField()
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"Slot for {self.ev_station_name} on {self.date} at {self.time} - {self.email}"


