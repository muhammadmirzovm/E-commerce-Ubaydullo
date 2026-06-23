from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Role", {'fields': ("role","phone_number", "image", 'address')}),
    )
    
    list_display = ('username', 'email', 'role')
    list_filter = ("role", )