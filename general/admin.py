from django.contrib import admin
from django.forms import ModelForm
from django.contrib.admin import ModelAdmin
from suit.widgets import SuitSplitDateTimeWidget

from .models import (
    Institution,
    Manufacturer
)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    pass


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass
