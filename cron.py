from apis.models import Event, EventRegistration,User
import datetime
from django.core.mail import send_mail
from decouple import config



def notassignedtoabsent(self):
    for event in Event.objects.all():
        end_date=event.end_datetime
        hour = int(end_date.hour)
        day = int(end_date.day)
        year = int(end_date.year)
        month = int(end_date.month)
        date = datetime.datetime(year,month,day,hour,0,0)
        now = datetime.datetime.now()
        for i in range(5):
            enddateplus1 = date+datetime.timedelta(days=1)
            enddateplus3 = date+datetime.timedelta(days=3)
        
        if enddateplus1 < now and enddateplus3 > now :
            for a in event.evre.all():
                if a.attendance == 0:
                    print(a)
                    print('yes')
                    a.attendance = 2
                    a.save()
                else:
                    print('NO')  

from datetime import datetime
import os
import django
from django.conf import settings
from django.core.management import call_command
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Shelf_Backend.settings")
django.setup()
import subprocess  # For executing a shell command
import requests

def backup():
    filename = datetime.now().strftime("Backup on %d-%m-%Y.psql")
    try:
        call_command("dbbackup")
        print( f"Backed up successfully: {datetime.now()}")
    except:
        print( f"Could not be backed up: {datetime.now()}")

def ping_database():
    db_name = config('DB_NAME')
    command = ['pg_isready', f'-d {db_name}']
    if subprocess.call(command) == 0 :
        pass
    else:
        subject = 'Database server is down!!!'
        message = 'Hi , Database server for shelf is down.'
        email_from = settings.EMAIL_FROM_ADDRESS
        recipient_list = ['raza.centrric@gmail.com', 'farhanfaizalmannighayil@gmail.com', 'jeffingbenny@gmail.com', 'faizsaleem10@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
        call_command('crontab remove')

def ping_webserver():
    try :
        response = requests.get('http://127.0.0.1/ping/')
        print(response.status_code)
    except :
        subject = 'Shelf Web server is down!!!'
        message = 'Hi , Webserver for shelf is down.'
        email_from = settings.EMAIL_FROM_ADDRESS
        recipient_list = ['raza.centrric@gmail.com', 'farhanfaizalmannighayil@gmail.com', 'jeffingbenny@gmail.com', 'faizsaleem10@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
        call_command('crontab remove')