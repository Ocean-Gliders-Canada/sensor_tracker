from django.contrib import admin
from platforms.models import (
    PlatformType,
)

from instruments.admin_filter import platform_type_list_ordered


class PlatformListFilter(admin.SimpleListFilter):
    title = 'Platform Type'

    parameter_name = 'platform_type'

    default_value = 'All'

    def lookups(self, request, model_admin):
        """Return a list of possible platform types and their respuctive PlatformType.id values
        """
        return platform_type_list_ordered()

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value() is None:
            return queryset
        else:
            return queryset.filter(platform_type__id=self.value())

    def value(self):
        """Return a default value, or the selected platform type
        """
        value = super(PlatformListFilter, self).value()
        if value is None:
            if self.default_value is None:
                # If there is at least one platform type, return the first by name. Otherwise, None.
                first_platform_type = PlatformType.objects.first()
                value = None if first_platform_type is None else first_platform_type.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)


class PlatformCommentBoxListFilter(PlatformListFilter):
    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value():
            if self.value() == 'All':
                return queryset
            else:
                return queryset.filter(platform__platform_type__id=self.value())


class PlatformDeploymentHasNumberFilter(admin.SimpleListFilter):
    """
    """
    title = 'Has number'

    parameter_name = 'has_number'

    ops = [
        ('any', 'Any'),
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    default_value = ops[0]

    def lookups(self, request, model_admin):
        return self.ops

    def queryset(self, request, queryset):
        if self.value():
            if self.value() == 'yes':
                return queryset.filter(deployment_number__isnull=False)
            elif self.value() == 'no':
                return queryset.filter(deployment_number__isnull=True)
        return queryset

    def value(self):
        value = super(PlatformDeploymentHasNumberFilter, self).value()
        if value is None:
            value = self.default_value
        return str(value)


class PlatformActiveFilter(admin.SimpleListFilter):
    title = 'active platform'

    parameter_name = 'active'

    def lookups(self, request, model_admin):
        """Return a list of possible platform types and their respuctive PlatformType.id values
        """
        return (
            ('1', (u'Yes')),
            ('2', (u'No')),
        )

    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value() is None:
            return queryset
        if self.value() == '1':
            return queryset.filter(active=True)
        if self.value() == '2':
            return queryset.filter(active=False)


class PlatformDeploymentCommentBoxListFilter(PlatformListFilter):
    def queryset(self, request, queryset):
        """Filter the queryset being returned based on the PlatformType that was selected
        """
        if self.value():
            if self.value() == 'All':
                return queryset
            else:
                return queryset.filter(platform_deployment__platform__platform_type__id=self.value())
