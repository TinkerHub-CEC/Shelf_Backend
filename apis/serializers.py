from rest_framework import serializers
from django.contrib.auth.models import User
from apis.models import Event, EventRegistration
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'email', 'password']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','title', 'datetime', 'location', 'max_participants', 'description']

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta :
        model = EventRegistration
        fields = ['id', 'user', 'event', 'attendance']