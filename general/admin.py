from django.contrib import admin
from custom_admin import admin as custom_admin_site
from .models import (
    Institution,
    Project,
    Manufacturer
)


class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'street', 'city', 'province', 'postal_code', 'country', 'contact_name', 'contact_phone',
        'contact_email',

        'url', 'created_date', 'modified_date',)
    readonly_fields = ('created_date', 'modified_date',)


custom_admin_site.site.register(Institution, InstitutionAdmin)


class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', 'modified_date',)


custom_admin_site.site.register(Project, ProjectAdmin)


class ManufacturerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'street', 'city', 'province', 'postal_code', 'country', 'contact_name', 'contact_phone',

        'contact_email',
        'created_date', 'modified_date')
    readonly_fields = ('created_date', 'modified_date',)


custom_admin_site.site.register(Manufacturer, ManufacturerAdmin)
