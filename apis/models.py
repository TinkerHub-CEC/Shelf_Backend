
from django.db import models
from django.db.models.base import Model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.enums import Choices


# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("user must have an email")
        if not username:
            raise ValueError('users must have username')

        user = self.model(
            email    = self.normalize_email(email),
            username = username, 
        )        

        user.set_password(password)
        user.save(using = self._db)
        return user


    def create_superuser(self,email,username,password):
            user = self.create_user(
                email = self.normalize_email(email),
                password = password,
                username = username,
            )
            user.is_admin = True
            user.is_staff = True
            user.is_superuser  = True
            user.save(using = self._db)
            return user
class User(AbstractBaseUser):
    SEMESTER_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    )

    BATCH_CHOICES = (
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
    ("F", "F"),
    ("G", "G"),
)


    email        = models.EmailField(verbose_name="email",max_length=60,unique=True)
    username     = models.CharField(max_length=30,unique=False,null=True,default=None)
    date_joined  = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login   = models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    first_name   = models.CharField(max_length=30,unique=False)
    last_name    = models.CharField(max_length=30,unique=False)
    roll_no      = models.CharField(max_length=20,unique=False)
    
    semester = models.CharField(
        max_length = 10,
        choices = SEMESTER_CHOICES,
        )


    batch = models.CharField(
        max_length=10,
        choices=BATCH_CHOICES, 
        )


    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username']
    

    objects = MyUserManager()

    def __str__(self) :
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True
        
class EventRegistration(models.Model):

    ATTENDANCE_ASSIGNMENT_CHOICES = (
        (0,'Not Assigned'), #Attendance Not Assigned
        (1,'Accepted'), #Attendance Accepted
        (2,'Rejected'), #Attendance Rejected
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete= models.CASCADE)
    attendance = models.IntegerField(default=0,choices=ATTENDANCE_ASSIGNMENT_CHOICES)
    photosubmission = models.ImageField(upload_to='pic',max_length = 200,null=True,blank=True)
    class Meta:
        unique_together = (('user','event'),)

class Event(models.Model) :
    ATTENDANCE_METHOD_CHOICES = (
        (0,'None'), #Default method : Null method
        (1,'CheckBox'), #CheckBox method
        (2,'Upload proof'), #UploadScreenshots method
    )
    title = models.CharField(max_length=30)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=30)
    max_participants = models.IntegerField()
    short_description = models.CharField(max_length=150)
    long_description = models.TextField()
    poster = models.ImageField(upload_to='uploads/events')
    reg_open_date = models.DateTimeField()
    reg_close_date = models.DateTimeField()
    registrations = models.ManyToManyField (User, through='EventRegistration', related_name='registered_events')
    attendance_method = models.IntegerField(default=0,choices=ATTENDANCE_METHOD_CHOICES)
    calender_event_id = models.CharField(max_length=100)

