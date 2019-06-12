from django.contrib import admin

from .models import (
    Institution,
    Project,
    Manufacturer
)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'street', 'city', 'province', 'postal_code', 'country', 'contact_name', 'contact_phone',
        'contact_email',
        'url', 'created_date', 'modified_date',)
    readonly_fields = ('created_date', 'modified_date',)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'modified_date',)


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'street', 'city', 'province', 'postal_code', 'country', 'contact_name', 'contact_phone',
        'contact_email',
        'created_date', 'modified_date')
    readonly_fields = ('created_date', 'modified_date',)
