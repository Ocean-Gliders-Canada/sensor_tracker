# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.authtoken.admin import TokenAdmin
from rest_framework.authtoken.models import Token

from custom_admin import admin as custom_admin_site

custom_admin_site.site.register(Token, TokenAdmin)
