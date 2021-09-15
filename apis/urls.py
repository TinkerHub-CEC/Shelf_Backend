from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views
from . import test
from django.conf import  settings
from django.conf.urls.static import static

urlpatterns = [
    #user authentication
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    #event details
    path('events/', views.event_list),
    path('events/active/all/',views.active_registrations),
    path('events/active/unregistered/',views.active_unregistered_events),
    path('events/<int:id>/', views.event_detail),
    path('events/<int:id>/registrations/', views.registered_users),
    path('events/<int:id>/register/', views.register_for_event),
    path('events/<int:id>/attendance/', views.mark_attendance),
    path('events/<int:id>/uploadimage/',views.upload_photo), 
    path('events/<int:id>/registrations_count/',views.event_registrations_count),
    path('events/active/all/',views.active_registrations),
    path('events/<int:id>/checkregistration/',views.registration_check),
    path('events/active/with_attendance/',views.active_events_with_attendance),
    

    #user details
    path('users/',views.user_list),
    path('users/<int:id>/',views.user_details),
    path('users/<int:id>/registered_events/',views.user_registered_events),


    #testing out new features
    path('test/',views.test),
    path('ping/',views.ping),
    
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL,document_root =settings.MEDIA_ROOT)
