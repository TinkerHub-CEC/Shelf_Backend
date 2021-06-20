from rest_framework import serializers
from apis.models import User, Event, EventRegistration
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

#Serializer class to inherit from, to dynamically change fields in a serializer
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
        fields = ['id','username', 'first_name', 'last_name', 'email', 'password','roll_no','semester','batch']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id','title', 'start_datetime', 'end_datetime', 'location','max_participants', 'short_description', 'long_description', 'reg_open_date',
                    'reg_close_date', 'poster']

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta :
        model = EventRegistration
        fields = ['id','photosubmission','user','event','attendance']

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        return token

    
