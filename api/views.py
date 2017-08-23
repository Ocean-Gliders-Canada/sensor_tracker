# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy
import json
import datetime

from django.apps import apps
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render


def get_deployments(request):
    deployments = apps.get_model('platforms', 'PlatformDeployment')
    gets = {}
    for get in request.GET:
        gets[get] = request.GET.get(get)
    if len(gets) == 0:
        res = deployments.objects.all()
    else:
        res = deployments.objects.filter(**gets).all()
    json_obj = {'data': []}
    for r in res:
        r_dict = copy.deepcopy(r.__dict__)
        del r_dict['_state']
        keys = r_dict.keys()
        to_add = []
        for key in keys:
            if 'id' in key and key != 'wmo_id':
                if key != 'id':
                    to_add.append(key.replace('_id', ''))
        for add in to_add:
            try:
                r_dict[add] = copy.deepcopy(getattr(r, add).__dict__)
                convert_times(r_dict[add])
                del r_dict[add]['_state']
            except AttributeError:
                pass  # It's a false alarm
        convert_times(r_dict)
        json_obj['data'].append(r_dict)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')
    # return serializers.serialize('json', deployments.objects.all())


# Helpers

def convert_times(obj):
    for k in obj:
        if type(obj[k]) == datetime.datetime:
            obj[k] = obj[k].strftime('%Y-%m-%d %H:%M:%S')
