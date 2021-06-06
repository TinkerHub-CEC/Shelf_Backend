
from django.db import models
from django.db.models.base import Model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


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
    username     = models.CharField(max_length=30,unique=False)
    date_joined  = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login   = models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey('Event', on_delete= models.CASCADE)
    attendance = models.IntegerField(default=0)
    photosubmission = models.ImageField(upload_to='pic',max_length = 200,)
    class Meta:
        unique_together = (('user','event'),)

class Event(models.Model) :
    title = models.CharField(max_length=30)
    datetime = models.DateTimeField()
    location = models.CharField(max_length=30)
    max_participants = models.IntegerField()
    description = models.TextField()
    registrations = models.ManyToManyField (User, through='EventRegistration', related_name='registered_events')

