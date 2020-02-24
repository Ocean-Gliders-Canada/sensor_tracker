from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin

from users.forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
