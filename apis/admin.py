from apis.forms import CustomUserChangeForm, RegistrationForm
from django.contrib import admin
from apis.models import Event, EventRegistration
from django.contrib.auth.admin import UserAdmin
from apis.models import User
# Register your models here.

class UserAdmin(UserAdmin):
    add_form = RegistrationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email','username','date_joined','last_login','is_admin','is_staff','first_name','last_name','roll_no','semester','batch')
    search_fields = ('email','username')
    readonly_fields = ('date_joined','last_login')


    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password','username','first_name','last_name','semester', 'batch')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','is_admin',)}
        ),
    )



admin.site.register(User,UserAdmin)
admin.site.register(Event)
admin.site.register(EventRegistration)
