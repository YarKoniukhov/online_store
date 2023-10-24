from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    model = UserProfile

    list_display = ('username', 'first_name', 'last_name', 'birth_date', 'phone', 'email', 'is_active', 'is_staff')

