from apis.models import Event, EventRegistration,User
import datetime 
from datetime import timedelta


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
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Stori10.settings")
django.setup()
import subprocess  # For executing a shell command
from services import mail
import requests

def backup():
    filename = datetime.now().strftime("Backup on %d-%m-%Y.psql")
    try:
        call_command("dbbackup")
        print( f"Backed up successfully: {datetime.now()}")
    except:
        print( f"Could not be backed up: {datetime.now()}")

def ping_database():
    command = ['pg_isready','-U postgres', '-d Shelf']
    if subprocess.call(command) == 1 :
        pass
    else:
        message_text = "Database server is down!!!"
        message_html = """\
                        <html>
                        <head></head>
                        <body>
                        <h1>Hello!</h1>
                        <p>Stori10 Database server is down.</p>
                        </body>
                        </html>
                        """
        mail.send_mail(message_text, message_html)

def ping_webserver():
    try :
        response = requests.get('http://127.0.0.1:8000/ping')
        print(response.status_code)
    except :
        print('Server down')
        message_text = "Web Server is down!!!"
        message_html = """\
                        <html>
                        <head></head>
                        <body>
                        <h1>Hello!</h1>
                        <p>Shelf Web server is down.</p>
                        </body>
                        </html>
                        """
        mail.send_mail(message_text, message_html)
ping_webserver()
ping_database()
# backup()