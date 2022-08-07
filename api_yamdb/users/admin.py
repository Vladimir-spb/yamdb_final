from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


UserAdmin.list_display += ('role', 'bio')

admin.site.register(User, UserAdmin)
