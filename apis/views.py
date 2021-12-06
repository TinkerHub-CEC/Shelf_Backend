import datetime 
from functools import partial
from django.http.response import JsonResponse
from rest_framework import fields, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from apis import serializers
from apis.models import Event, EventRegistration ,User
from apis.serializers import EventSerializer, EventRegistrationSerializer, UserSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt import views as jwt_views
from django.conf import settings
from django.core.mail import send_mail
from django_email_verification import send_email as send_verification_mail
from api_paginator.api_paginator import paginate
from services.google_calender import calender_services as calender
from datetime import datetime, timedelta
import threading



@api_view(['GET', 'POST'])
#@permission_classes((IsAuthenticated, ))
def test(request, format=None):
    #test new features here
    r = 7/0
    return False

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def event_list(request, format=None):
    """
    List all events, or create a new event.
    """
    try:
        if request.method == 'GET':
            try:
                page = int(request.query_params.get('page'))
            except:
                page = 1
            try:
                limit = int(request.query_params.get('limit'))
            except:
                limit = 10
            if request.user.is_admin == 0:
                events = Event.objects.order_by('-start_datetime')
                serializer = EventSerializer(events, many=True,context={'user_id': request.user.id})
                result = paginate(serializer.data, page, limit)
                return Response(result)
            else :
                events = Event.objects.filter(organization = request.user.organization)
                serializer = EventSerializer(events, many=True,context={'user_id': request.user.id})
                result = paginate(serializer.data, page, limit)
                return Response(result)


        elif request.method == 'POST':
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                event_obj = serializer.save()
                event_obj.organization = request.user.organization
                event_obj.save()

                #Calling Function in a new thread to create a cooresponding event in google calender
                t1 = threading.Thread(target=create_event_g_calender, args=(event_obj,))
                t1.start()
                
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def event_detail(request, id, format=None):
    """
    Retrieve, update or delete a event
    """
    try: 
        try:
            event_obj = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response({'dev_data': f'Event with id={id} does not exist!', 'app_data': 'Event not found!'},status=status.HTTP_404_NOT_FOUND)
    
        if request.method == 'GET':
            serializer = EventSerializer(event_obj, context={'user_id': request.user.id})
            return Response(serializer.data)
    
        elif request.method == 'PUT':
            serializer = EventSerializer(event_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        elif request.method == 'DELETE':
            event_obj.delete()
            return Response({'dev_data': 'Event deleted succesfully!',},status=status.HTTP_204_NO_CONTENT) 
        
    except Exception as e: 
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def registered_users(request, id, format=None):
    """
    View registered users of a particular event, if event id is provided
    """
    try: 
        try:
            event_obj = Event.objects.get(id=id)
            registered_users = event_obj.registrations.all()
        except Event.DoesNotExist:
            return Response({'dev_data': f'Event with id={id} does not exist!', 'app_data': 'Event not found!'},status=status.HTTP_404_NOT_FOUND)
    
        if request.method == 'GET':
            serializer = UserSerializer(registered_users, many=True, fields=('id', 'first_name', 'last_name', 'semester', 'batch', 'email'))
            return Response(serializer.data) 
        
    except Exception as e:
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def register_for_event(request, id, format=None):
    """
    Create a new registration for an event or delete an existing registration
    """
    try: 
        try:
            event_obj = Event.objects.get(id=id)
        except Event.DoesNotExist:
            return Response({'dev_data': f'Event with id={id} does not exist!', 'app_data': 'Event not found!'},status=status.HTTP_404_NOT_FOUND)
    
        if request.method == 'POST':
            event_obj.registrations.add(request.user)

            #Sending Email to Registered User
            subject = f'You have registered for {event_obj.title}'
            message = f'Hi , thank you for registering in {event_obj.title}.'
            email_from = settings.EMAIL_FROM_ADDRESS
            recipient_list = [request.user.email ]
            t1 = threading.Thread(target=send_mail, args=(subject, message,email_from,recipient_list))
            t1.start()

            #Adding user to the corresponding event created in google calender
            user_email = { 'email': f'{request.user.email}' }
            t2 = threading.Thread(target=calender.update_event, args=(event_obj,user_email))
            t2.start()
            
            return Response(status=status.HTTP_201_CREATED)
        
        if request.method == 'DELETE' :
            event_obj.registrations.remove(request.user)
            return Response(status=status.HTTP_204_NO_CONTENT) 
    
    except Exception as e: 
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view([ 'POST' ])
def user_list(request,format=None):
    """
    Create new User object.
    """
    #Create new User object
    try: 
        if request.method == 'POST':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user_obj = serializer.save()
                user_obj.set_password(user_obj.password)
                user_obj.is_active = False
                user_obj.save()
                send_verification_mail(user_obj)
                print('Verification email sent')
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST) 
    
    except Exception as e: 
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def user_details(request, id, format=None):
    """
    Retrieve, delete, update a single users' details
    """
    try: 
        try:
            user_obj = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'dev_data': f'User with id={id} does not exist!', 'app_data': 'User not found!'},status=status.HTTP_404_NOT_FOUND)
    
        #Get details of a single user
        if request.method == 'GET':
            serializer = UserSerializer(user_obj)
            return Response(serializer.data)
    
        #Update details of a single user
        elif request.method == 'PUT':
            serializer = UserSerializer(user_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        #Delete details of a single user
        elif request.method == 'DELETE':
            user_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) 
    
    except Exception as e: 
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['PUT','GET'])
@permission_classes((IsAuthenticated, ))
def mark_attendance(request,id):

    if request.method == 'GET':
        try:
            reg_objs = EventRegistration.objects.filter(event=id,attendance=0)
        except EventRegistration.DoesNotExist:
            return Response({'dev_data': f'Event Registration with id={id} does not exist!', 'app_data': 'Event not found!'},status=status.HTTP_404_NOT_FOUND)
        
        display =list()
        for obj in reg_objs:
            if obj.photosubmission == '':
                pass
            else:
                details = dict()
                individual_user = User.objects.get(id=obj.user.id)
                user_serializer = UserSerializer(individual_user, read_only=True,fields=('id','first_name','last_name','semester','batch'))
                eventreg_serializer = EventRegistrationSerializer(obj,read_only=True,fields=('user','photosubmission','attendance'))
                details = user_serializer.data
                details.update(eventreg_serializer.data)
                display.append(details)
        return Response(display)

    if request.method == 'PUT':
        try:
            user = request.POST.get('user')
            reg_obj = EventRegistration.objects.get(user=user, event=id)
        except EventRegistration.DoesNotExist:
            return Response({'dev_data': f'Event Registration object with event id={id} and user id= {user} Doesnot Exist!', 'app_data': 'Something went wrong!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EventRegistrationSerializer(reg_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes((IsAuthenticated, ))
def upload_photo(request,id,format=None):

    try:
        try:
            instance = EventRegistration.objects.get(event=id, user=request.user)
        except:
            return Response({'dev_data': f'No active registration found for event_id={id} with current logged in user!', 'app_data': 'Not registered in event!'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = EventRegistrationSerializer(instance,data = request.data,partial = True)   
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    except Exception as e: 
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view([ 'GET' ])
@permission_classes((IsAuthenticated, ))
def user_registered_events(request, id, format=None):
    """
    Function that returns all the events that a user is registered to.
    """
    try: 
        try:
            user = User.objects.get(id=id)
            registered_events = user.registered_events.all()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.method == 'GET':
            serializer = EventSerializer(registered_events, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK) 
    
    except Exception as e: 
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def active_unregistered_events(request, format=None):

    # Function that returns all active events that a user is not registered to.

    try: 
        if request.method == 'GET':
            user = User.objects.get(id=request.user.id)
            user_registered_events = user.registered_events.all()
            active_registrations = Event.objects.filter(reg_open_date__lt=datetime.now(),reg_close_date__gt=datetime.now())
            active_unregistered_events = active_registrations.difference(user_registered_events)
            serializer = EventSerializer(active_unregistered_events, many=True)
            return Response(serializer.data)
        else :
            return Response("Scene ahnello") 
    
    except Exception as e: 
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def event_registrations_count(request, id, format=None):
    """
    Total number of users registered in a particular event, if event id is provided.
    """
    try: 
        try:
            event_obj = Event.objects.get(id=id)
            registered_users = event_obj.registrations.all()
            user_count = registered_users.count()
        except Event.DoesNotExist:
            return Response({'dev_data': f'Event with id={id} does not exist!', 'app_data': 'Event doesnot exist!'},status=status.HTTP_404_NOT_FOUND)
    
        if request.method == 'GET':
            return Response({"count" : user_count}) 
    
    except Exception as e: 
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def active_registrations(request,format=None):
    try: 
        if request.method == 'GET':
            active_registrations = Event.objects.filter(reg_open_date__lt=datetime.now(),reg_close_date__gt=datetime.now())
            serializer = EventSerializer(active_registrations, many=True)
            return Response(serializer.data) 
    
    except Exception as e: 
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def registration_check(request,id):
    try:
        try:
            instance = EventRegistration.objects.get(event=id, user=request.user)
            return Response(True)
        except:
            return Response(False)
    except Exception as e: 
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def active_events_with_attendance(request,format=None):

    # This returns all events which the user have registered and have attendance method of checkbox or upload image

    try: 
        if request.method == 'GET':
            active_registrations = Event.objects.filter(evre__user=request.user,end_datetime__lt=datetime.now(),evre__attendance=0,evre__photosubmission = '').exclude(attendance_method = 0)
            serializer = EventSerializer(active_registrations, many=True)
            return Response(serializer.data)

    
    except Exception as e: 
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def events_to_verify_attendance(request,format=None):

    # This returns all events which the user have registered and have attendance method of checkbox or upload image

    try: 
        if request.method == 'GET':
            active_registrations = Event.objects.filter(organization = request.user.organization,attendance_method = 2,end_datetime__range=[(datetime.now()-timedelta(days=10)),datetime.now()])
            serializer = EventSerializer(active_registrations, many=True)
            return Response(serializer.data)

    
    except Exception as e: 
        return Response({'dev_data': str(e), 'app_data': 'Something went wrong!'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#Custom JWT token to distinguish user type(normal or admin user)
class CustomTokenObtainPairView(jwt_views.TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer
    token_obtain_pair = jwt_views.TokenObtainPairView.as_view()

def create_event_g_calender(event_obj):
    calender_event_id = calender.create_event(event_obj)
    event_obj.calender_event_id = calender_event_id
    event_obj.save()
#Respond with 200 ok when pinged
@api_view(['GET'])
def ping(request) :
    return Response(status=status.HTTP_200_OK)
        
       
    


    




