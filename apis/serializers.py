from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from apis.models import Account, Event, EventRegistration
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id','username', 'last_name', 'email', 'password','roll_no','semester','batch']
        write_only_fields = ['password']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','title', 'datetime', 'location', 'max_participants', 'description']

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta :
        model = EventRegistration
        fields = ['id', 'user', 'event', 'attendance']


