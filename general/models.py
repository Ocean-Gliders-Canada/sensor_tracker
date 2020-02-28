from django.db import models
from common.model import ModelBase


class Institution(ModelBase):
    # Name of the institution
    name = models.CharField(
        max_length=300,
        help_text="Name of the institution",
        unique=True
    )
    # re.match(r'(https?(://)?)?(?P<url>.*)', url)
    url = models.CharField(
        max_length=1000,
        help_text="The institution's URL",
        blank=True, null=True
    )
    # Location of the institution
    street = models.TextField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    province = models.CharField(max_length=80, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=80, blank=True, null=True)
    # Contact at the institution
    contact_name = models.CharField(max_length=70, blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Project(ModelBase):
    name = models.CharField(
        max_length=1000,
        help_text="<b>Example:</b> Collaborative Operations with Mote Marine Laboratory",
        unique=True
    )

    def __str__(self):
        return self.name


class Manufacturer(ModelBase):
    name = models.CharField(max_length=300, unique=True)
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
