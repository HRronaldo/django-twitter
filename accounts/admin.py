from django.contrib import admin
from django.contrib.auth.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_joined'
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'last_login',
    )
