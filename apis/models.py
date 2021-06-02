
from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User

# Create your models here.

class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete= models.CASCADE)
    attendance = models.IntegerField(default=0)
    class Meta:
        unique_together = (('user','event'),)

class Event(models.Model) :
    title = models.CharField(max_length=30)
    datetime = models.DateTimeField()
    location = models.CharField(max_length=30)
    max_participants = models.IntegerField()
    description = models.TextField()
    registrations = models.ManyToManyField (User, through='EventRegistration', related_name='registered_events')

