from __future__ import unicode_literals

from django.db import models


class PlatformType(models.Model):
    model = models.CharField(max_length=300)
    manufacturer = models.ForeignKey('general.Manufacturer', on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.model, self.manufacturer)


class Platform(models.Model):
    name = models.CharField(
        max_length=300,
        help_text="The colloquial name for the platform"
    )
    serial_number = models.CharField(max_length=300)
    platform_type = models.ForeignKey(PlatformType, on_delete=models.CASCADE)
    institution = models.ForeignKey(
        'general.Institution',
        on_delete=models.CASCADE,
        help_text="The institution who owns the platform"
    )
    purchase_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.name, self.serial_number)


class PlatformComment(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    comment = models.TextField(
        help_text="This is a good place to log any problems or changes with a platform"
    )
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.instrument, self.created_date)


class PlatformDeployment(models.Model):
    deployment_number = models.IntegerField(null=True, blank=True)
    platform = models.ForeignKey(Platform)
    start_time = models.DateTimeField(null=False, blank=False)
    deployment_name = models.CharField(max_length=150)
    end_time = models.DateTimeField(null=True, blank=True)
    comment = models.TextField()

    def __str__(self):
        if self.deployment_name is not None:
            return "%s - %s - %s" % (
                self.deployment_name,
                self.platform.name,
                self.start_time
            )
        else:
            return "%s - %s" % (
                self.platform.name,
                self.start_time
            )


class PlatformDeploymentComment(models.Model):
    platform_deployment = models.ForeignKey(PlatformDeployment, on_delete=models.CASCADE)
    comment = models.TextField(
        help_text="This is a good place to log any changes to a deployment"
    )
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.instrument, self.created_date)
