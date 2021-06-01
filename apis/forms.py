from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms import fields
from apis.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60,help_text="required add a valid email address")


    class meta:
        model = Account
        fields = ("email",)



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Account
        fields = ('email',)