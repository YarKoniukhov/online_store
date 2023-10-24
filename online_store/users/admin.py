from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


User = get_user_model()


@admin.register(User)
class UserProfileAdmin(UserAdmin):

    list_display = ('username', 'first_name', 'last_name', 'birth_date',
                    'phone', 'email', 'city', 'department_np', 'is_active', 'is_staff')

