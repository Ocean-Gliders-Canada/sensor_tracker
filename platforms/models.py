from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.admin import User


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


class PlatformPowerType(models.Model):
    name = models.CharField(
        max_length=500,
        help_text="Power source of this deployment"
    )

    def __str__(self):
        return "%s" % (self.name)


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
    power_type = models.ForeignKey(
        PlatformPowerType,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text="The battery type which was using in this deployment."
    )

    platform_name = models.CharField(
        max_length=500,
        help_text="Name of platform.",
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=500,
        help_text="A short descriptive title for the deployment."
    )
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=True, blank=True)
    is_task_mission = models.BooleanField(
        default=False,
        help_text="if this is task mission, check this."
    )
    comment = models.TextField(null=True,
                               blank=True,
                               help_text="The general comments for the deployment."
                               )

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
    creator_email = models.TextField(
        help_text="The email of person collected data.",
        null=True,
        blank=True
    )
    creator_name = models.TextField(
        help_text="A comma separated of names of the person who collected the data.",
        null=True,
        blank=True
    )
    creator_url = models.TextField(
        help_text="A comma separated of URLs for the person who collected the data.",
        null=True,
        blank=True
    )
    data_repository_link = models.CharField(
        max_length=150,
        help_text="URL for the repository from:  <a href='http://belafonte.ocean.dal.ca:8080/erddap/index.html'>Erddap</a>.",
        null=True,
        blank=True
    )
    publisher_email = models.CharField(
        max_length=150,
        help_text="E-mail address of the publisher of the data.",
        null=True,
        blank=True
    )
    publisher_name = models.CharField(
        max_length=150,
        help_text="Name of the publisher of the data.",
        null=True,
        blank=True
    )
    publisher_url = models.CharField(
        max_length=150,
        help_text="A URL for the publisher of the data.",
        null=True,
        blank=True
    )
    metadata_link = models.CharField(
        max_length=150,
        help_text="This attribute provides a link to a complete metadata record for this data set or the collection that contains this data set.",
        null=True,
        blank=True
    )
    references = models.TextField(
        help_text="Published or web-based references that describe the data or methods used to produce it.",
        null=True,
        blank=True,
    )
    sea_name = models.CharField(
        max_length=300,
        help_text="The sea in which the study is being conducted: <a href='https://www.nodc.noaa.gov/General/NODC-Archive/seanamelist.txt'>Sea Names</a>",
        default="North Atlantic Ocean"
    )

    latitude = models.FloatField(
        null=True,
        blank=True,
        help_text='The latitude of the deployment'
    )

    longitude = models.FloatField(
        null=True,
        blank=True,
        help_text='The longitude of the deployment'
    )

    depth = models.FloatField(
        null=True,
        blank=True,
        help_text='The depth of the deployment'
    )

    def __str__(self):
        return_string = ''
        if self.title is not None:
            return_string += '%s - ' % self.title
        return_string += '%s - %s' % (
            self.platform_name,
            self.start_time.strftime('%Y-%m-%d')
        )
        if self.end_time is not None:
            return_string += ' - %s' % self.end_time.strftime('%Y-%m-%d')
        return return_string


class PlatformDeploymentCommentBox(models.Model):
    platform_deployment = models.OneToOneField('PlatformDeployment', on_delete=models.PROTECT)

    def __str__(self):
        return "%s comment box" % (self.platform_deployment)


class PlatformDeploymentComment(models.Model):
    user = models.ForeignKey(User)
    comment = models.TextField(help_text="Comments")
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    platform_deployment_comment_box = models.ForeignKey(PlatformDeploymentCommentBox)

    def __str__(self):
        return "%s" % (self.id)


class PlatformCommentBox(models.Model):
    platform = models.OneToOneField('Platform', on_delete=models.PROTECT)

    def __str__(self):
        return "%s comment box" % (self.platform)


class PlatformComment(models.Model):
    user = models.ForeignKey(User)
    comment = models.TextField(
        help_text="This is a good place to log any problems or changes with a platform"
    )
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    platform_comment_box = models.ForeignKey(PlatformCommentBox)

    def __str__(self):
        return "%s" % (self.id)
