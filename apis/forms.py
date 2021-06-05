from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import fields
from apis.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60,help_text="required add a valid email address")


    class meta:
        model = User
        fields = ("email",)



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)

