from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')  # Add other fields as needed
    search_fields = ('username', 'email')

admin.site.register(User, UserAdmin)