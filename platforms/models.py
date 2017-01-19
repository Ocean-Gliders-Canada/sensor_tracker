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
        help_text="The name of the platform"
    )
    wmo_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="The WMO ID for the mission. See: <a href='http://www.jcomm.info/index.php?option=com_oe&task=viewGroupRecord&groupID=155'>WMO Contact Info</a> to acquire"
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
    wmo_id = models.IntegerField(
        null=True,
        blank=True,
        help_text="The WMO ID for the mission. See: <a href='http://www.jcomm.info/index.php?option=com_oe&task=viewGroupRecord&groupID=155'>WMO Contact Info</a> to acquire"
    )
    deployment_number = models.IntegerField(null=True, blank=True)
    platform = models.ForeignKey(Platform)
    institution = models.ForeignKey(
        'general.Institution',
        on_delete=models.PROTECT,
        help_text="The institution responsible for the deployment."
    )
    project = models.ForeignKey(
        'general.Project',
        on_delete=models.PROTECT,
        help_text="The project the data is being collected under."
    )
    title = models.CharField(
        max_length=500,
        help_text="A short descriptive title for the deployment."
    )
    start_time = models.DateTimeField(null=False, blank=False)
    deployment_name = models.CharField(max_length=150)
    end_time = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    acknowledgement = models.CharField(
        max_length=900,
        help_text="<b>Example:</b> This deployment is supported by funding from NOAA",
        null=True,
        blank=True
    )
    contributor_name = models.TextField(
        help_text="A comma separated list of contributors to this data set<br><b>Example:</b> \"Jerry Garcia, Bob Weir, Bill Graham\"",
        null=True,
        blank=True
    )
    contributor_role = models.TextField(
        help_text="A comma separated list of the roles for those specified in the contributor_name attribute<br><b>Example:</b> \"Principal Investigator, Principal Investigator, Data Manager\"",
        null=True,
        blank=True
    )
    creator_email = models.CharField(
        max_length=150,
        help_text="Email address for the person who collected the data.",
        null=True,
        blank=True
    )
    creator_name = models.CharField(
        max_length=150,
        help_text="Name of the person who collected the data.",
        null=True,
        blank=True
    )
    creator_url = models.CharField(
        max_length=150,
        help_text="URL for the person who collected the data.",
        null=True,
        blank=True
    )
    sea_name = models.CharField(
        max_length=300,
        help_text="The sea in which the study is being conducted: <a href='https://www.nodc.noaa.gov/General/NODC-Archive/seanamelist.txt'>Sea Names</a>",
        default="North Atlantic Ocean"
    )

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
