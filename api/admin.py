# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.authtoken.admin import TokenAdmin

from django.forms import ModelForm


class TokenForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial:
            self.initial["user"] = self.instance.user


def get_queryset(self, request):
    user = request.user
    qs = self.model._default_manager.get_queryset()
    ordering = self.get_ordering(request)
    if ordering:
        qs = qs.order_by(*ordering)

    if not user.is_superuser:
        qs = qs.filter(user=user)
    return qs


TokenAdmin.form = TokenForm
TokenAdmin.get_queryset = get_queryset
