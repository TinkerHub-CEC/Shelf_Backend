from apis.models import Event, EventRegistration,User
import datetime 


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