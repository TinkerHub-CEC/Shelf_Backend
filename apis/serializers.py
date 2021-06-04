from rest_framework import serializers
from apis.models import User, Event, EventRegistration

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
                
class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'last_name', 'email', 'password','roll_no','semester','batch']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','title', 'datetime', 'location', 'max_participants', 'description']

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta :
        model = EventRegistration
        fields = ['id', 'user', 'event', 'attendance']

