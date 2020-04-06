from django.db import models


class ModelBase(models.Model):
    class Meta:
        abstract = True

    """
    Most of our model has modified date and create date
    """
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, null=True, blank=True)


class CommentModelBase(ModelBase):
    class Meta:
        abstract = True

    event_time = models.DateTimeField(null=True, blank=True)
