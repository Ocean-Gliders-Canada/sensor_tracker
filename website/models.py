from __future__ import unicode_literals
from django.db import models


class Institution(models.Model):
    # Name of the institution
    name = models.CharField(
        max_length=300,
        help_text="Name of the institution"
    )
    # Location of the institution
    street = models.TextField(max_length=255)
    city = models.CharField(max_length=40)
    province = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=80)
    # Contact at the institution
    contact_name = models.CharField(max_length=70, null=True, blank=True)
    contact_phone = models.CharField(max_length=15, null=True, blank=True)
    contact_email = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class PlatformType(models.Model):
    model = models.CharField(max_length=300, null=False)
    manufacturer = models.CharField(max_length=300, null=False)

    def __str__(self):
        return "%s - %s" % (self.model, self.manufacturer)


class Platform(models.Model):
    name = models.CharField(
        max_length=300,
        help_text="The colloquial name for the platform"
    )
    manufacturer_name = models.CharField(
        max_length=300,
        null=True,
        help_text="The formal name for the platform given by the manufacturer"
    )
    serial_number = models.CharField(max_length=300)
    platform_type = models.ForeignKey(PlatformType, on_delete=models.CASCADE)
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        help_text="The institution who owns the platform"
    )
    purchase_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.name, self.serial_number)


class Instrument(models.Model):
    manufacturer_name = models.CharField(
        max_length=300,
        help_text="The name given to the instrument by the manufacturer"
    )
    short_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="The short, general name for the instrument. IE: ctd, fluorometer"
    )
    long_name = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        help_text="The official, standard name for the instrument if relevant"
    )
    manufacturer = models.CharField(max_length=300, null=True, blank=True)
    serial = models.CharField(max_length=300, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.manufacturer_name


class InstrumentOnPlatform(models.Model):
    instrument = models.ForeignKey(
        Instrument,
        help_text="The instrument that was put on a platform"
    )
    platform = models.ForeignKey(
        Platform,
        help_text="The platform that the instrument was put on"
    )
    start_time = models.DateTimeField(
        null=False,
        blank=False,
        help_text="The date the instrument was put on the platform"
    )
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The date the instrument was removed from the platform"
    )
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s - %s - %s" % (self.instrument, self.platform, self.start_date)


class PlatformDeployment(models.Model):
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


class Sensor(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    manufacturer_name = models.CharField(
        max_length=300,
        help_text="The name given to the instrument by the manufacturer. ie: sci_water_temp"
    )
    short_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="The short, general name for the sensor. IE: temperature"
    )
    long_name = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        help_text="The official, standard name for the instrument. IE: sea_water_temperature. See CF naming: http://cfconventions.org/Data/cf-standard-names/39/build/cf-standard-name-table.html"
    )
    units = models.CharField(max_length=30, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.wgms_name, self.instrument.wgms_name)
