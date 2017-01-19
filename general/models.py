from __future__ import unicode_literals

from django.db import models


class Institution(models.Model):
    # Name of the institution
    name = models.CharField(
        max_length=300,
        help_text="Name of the institution"
    )
    url = models.CharField(
        max_length=1000,
        help_text="The institution's URL"
    )
    # Location of the institution
    street = models.TextField(max_length=255)
    city = models.CharField(max_length=40)
    province = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=80)
    # Contact at the institution
    contact_name = models.CharField(max_length=70, blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(
        max_length=1000,
        help_text="<b>Example:</b> Collaborative Operations with Mote Marine Laboratory"
    )

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=300)
    street = models.TextField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    province = models.CharField(max_length=80, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=80, blank=True, null=True)
    # Contact at the manufacturer
    contact_name = models.CharField(max_length=70, blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
