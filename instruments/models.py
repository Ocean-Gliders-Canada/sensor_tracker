from __future__ import unicode_literals

from django.db import models


class Instrument(models.Model):
    identifier = models.CharField(
        max_length=300,
        help_text="The name used to identify this instrument in the raw data. IE: SATCTD7229, sea_water"
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
        help_text="The full name for the instrument"
    )
    manufacturer = models.CharField(max_length=300, null=True, blank=True)
    serial = models.CharField(max_length=300, null=True, blank=True)
    master_instrument = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    comment = models.TextField(
        null=True,
        blank=True,
        help_text="This is a good place to document anything unusual about this instrument's configuration"
    )
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.manufacturer_name


class InstrumentComment(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    comment = models.TextField(
        help_text="This is a good place to log any problems or changes with an instrument"
    )
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.instrument, self.created_date)


class InstrumentOnPlatform(models.Model):
    instrument = models.ForeignKey(
        Instrument,
        help_text="The instrument that was put on a platform"
    )
    platform = models.ForeignKey(
        'platforms.Platform',
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


class Sensor(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    identifier = models.CharField(
        max_length=300,
        help_text="The name used to identify this sensor in the raw data. ie: sci_water_temp"
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
        help_text="The official, standard name for the instrument. IE: sea_water_temperature. See CF naming: <a href='http://cfconventions.org/Data/cf-standard-names/39/build/cf-standard-name-table.html'>CF Naming Reference</a>"
    )
    units = models.CharField(max_length=30, null=True, blank=True)
    include_in_output = models.BooleanField(
        default=False,
        help_text="Whether or not data from this sensor should be included in any processed output."
    )
    comment = models.TextField(
        null=True,
        blank=True,
        help_text="This is a good place to document anything unusual about this particular sensor. IE: wavelengths for spectral sensors"
    )
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return "%s - %s" % (self.wgms_name, self.instrument.wgms_name)
