from rest_framework import fields, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apis.models import Event, EventRegistration
from apis.serializers import EventSerializer, EventRegistrationSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User


# Create your views here.
@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated, ))
def event_list(request, format=None):
    """
    List all events, or create a new event.
    """
    if request.method == 'GET':
        events = Event.objects.order_by('-datetime')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
#@permission_classes((IsAuthenticated, ))
def event_detail(request, id, format=None):
    """
    Retrieve, update or delete a event
    """
    try:
        event_obj = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event_obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = EventSerializer(event_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        event_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
#@permission_classes((IsAuthenticated, ))
def event_registrations(request, id, format=None):
    """
    View registered users of a particular event, if event id is provided
    """
    try:
        event_obj = Event.objects.get(id=id)
        registered_users = event_obj.registrations.all()
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(registered_users, many=True, fields=('id', 'first_name', 'email'))
        return Response(serializer.data)

@api_view(['POST', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def register_for_event(request, id, format=None):
    """
    Create a new registration for an event or delete an existing registration
    """
    try:
        event_obj = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        event_obj.registrations.add(request.user)
        return Response(status=status.HTTP_201_CREATED)
    if request.method == 'DELETE' :
        event_obj.registrations.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view([ 'GET' , 'POST' ])
def user_list(request,format=None):
    """
    List all Users. Create new User object.
    """
    #Get all users' details
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    #Create new User object
    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_details(request, id, format=None):
    """
    Retrieve, delete, update a single users' details
    """
    try:
        user_obj = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #Get details of a single user
    if request.method == 'GET':
        serializer = UserSerializer(user_obj)
        return Response(serializer.data)

    #Update details of a single user
    elif request.method == 'PUT':
        serializer = UserSerializer(user_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #Delete details of a single user
    elif request.method == 'DELETE':
        user_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)