# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import datetime

from django.apps import apps
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render


def get_deployments(request, plat_name=None):
    deployments = apps.get_model('platforms', 'PlatformDeployment')
    if plat_name is None:
        res = deployments.objects.values()
    else:
        res = deployments.objects.filter(platform__name=plat_name).values()
    json_obj = {'data': []}
    for r in res:
        if type(r['start_time']) is datetime.datetime:
            r['start_time'] = r['start_time'].strftime('%Y-%m-%d %H:%M:%S')
        if type(r['end_time']) is datetime.datetime:
            r['end_time'] = r['end_time'].strftime('%Y-%m-%d %H:%M:%S')
        json_obj['data'].append(r)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')
    # return serializers.serialize('json', deployments.objects.all())
