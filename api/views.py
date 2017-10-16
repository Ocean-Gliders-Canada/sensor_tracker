# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy
import json
import datetime

from django.apps import apps
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q


# GET Requests

def get_deployments(request):
    Deployment = apps.get_model('platforms', 'PlatformDeployment')
    gets = {}
    for get in request.GET:
        gets[get] = request.GET.get(get)
    if len(gets) == 0:
        res = Deployment.objects.all()
    else:
        res = Deployment.objects.filter(**gets).all()
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')
    # return serializers.serialize('json', Deployment.objects.all())


def get_instruments(request):
    Instrument = apps.get_model('instruments', 'Instrument')

    if len(request.GET) == 0:
        res = Instrument.objects.all()
    else:
        gets = {}
        if 'id' in request.GET:
            gets['id'] = request.GET.get('id')
        if 'identifier' in request.GET:
            gets['identifier'] = request.GET.get('identifier')
        res = Instrument.objects.filter(**gets)
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


def get_instruments_on_platform(request):
    InstrumentOnPlatform = apps.get_model('instruments', 'InstrumentOnPlatform')

    if len(request.GET) == 0:
        res = InstrumentOnPlatform.objects.all()
    else:
        query = None
        if 'id' in request.GET:
            query = Q(id=request.GET.get('id'))
        if 'name' in request.GET:
            if query is None:
                query = Q(platform__name=request.GET.get('name'))
            else:
                query &= Q(platform__name=request.GET.get('name'))
        if 'time' in request.GET:
            try:
                g_time = format_time(request.GET.get('time'))
            except Exception:
                error = {'error': 'Time format: Y-m-d H:M:S. %s doesn\'t fit.' % request.GET.get('time')}
                return HttpResponse(json.dumps(error), content_type='application/json')
            if query is None:
                query = Q(start_time__lte=g_time) & (Q(end_time__gte=g_time) | Q(end_time=None))
            else:
                query &= Q(start_time__lte=g_time) & (Q(end_time__gte=g_time) | Q(end_time=None))
        if 'identifier' in request.GET:
            if query is None:
                query = Q(instrument__identifier=request.GET.get('identifier'))
            else:
                query &= Q(instrument__identifier=request.GET.get('identifier'))
        if query is not None:
            res = InstrumentOnPlatform.objects.filter(query)
        else:
            error = {'error': 'No valid arguments were provided.'}
            return HttpResponse(json.dumps(error), content_type='application/json')
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


def get_sensors(request):
    Sensor = apps.get_model('instruments', 'Sensor')
    if len(request.GET) == 0:
        res = Sensor.objects.all()
    else:
        gets = {}
        if 'id' in request.GET:
            gets['id'] = request.GET.get('id')
        if 'identifier' in request.GET:
            gets['identifier'] = request.GET.get('identifier')
        res = Sensor.objects.filter(**gets)
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


def get_platform(request):
    Platform = apps.get_model('platforms', 'Platform')
    if len(request.GET) == 0:
        res = Platform.objects.all()
    else:
        gets = {}
        if 'id' in request.GET:
            gets['id'] = request.GET.get('id')
        if 'name' in request.GET:
            gets['name'] = request.GET.get('name')
        res = Platform.objects.filter(**gets)
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


def get_manufacturer(request):
    Manufacturer = apps.get_model('general', 'Manufacturer')
    if len(request.GET) == 0:
        res = Manufacturer.objects.all()
    else:
        gets = {}
        if 'id' in request.GET:
            gets['id'] = request.GET.get('id')
        if 'name' in request.GET:
            gets['name'] = request.GET.get('name')
        res = Manufacturer.objects.filter(**gets)
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


def get_institutions(request):
    Institution = apps.get_model('general', 'Institution')
    if len(request.GET) == 0:
        res = Institution.objects.all()
    else:
        gets = {}
        if 'id' in request.GET:
            gets['id'] = request.GET.get('id')
        if 'name' in request.GET:
            gets['name'] = request.GET.get('name')
        res = Institution.objects.filter(**gets)
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


def get_project(request):
    Project = apps.get_model('general', 'Project')
    if len(request.GET) == 0:
        res = Project.objects.all()
    else:
        gets = {}
        if 'id' in request.GET:
            gets['id'] = request.GET.get('id')
        if 'name' in request.GET:
            gets['name'] = request.GET.get('name')
        res = Project.objects.filter(**gets)
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


def get_platform_type(request):
    PlatformType = apps.get_model('platforms', 'PlatformType')
    Platform = apps.get_model('platforms', 'Platform')
    if len(request.GET) == 0:
        res = PlatformType.objects.all()
    else:
        if 'model' in request.GET and 'name' in request.GET:
            error = {'error': 'Must choose either model or platform name to search by, not both.'}
            return HttpResponse(json.dumps(error), content_type='application/json')
        if 'model' in request.GET:
            res = PlatformType.objects.filter(model=request.GET.get('model'))
        elif 'name' in request.GET:
            name = request.GET.get('name')
            platforms = Platform.objects.filter(name=name)
            type_ids = []
            for platform in platforms:
                type_ids.append(platform.platform_type_id)
            res = PlatformType.objects.filter(id__in=type_ids)
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


def get_platform_deployments(request):
    PlatformDeployment = apps.get_model('platforms', 'PlatformDeployment')
    if len(request.GET) == 0:
        res = PlatformDeployment.objects.all()
        json_obj = {}
        json_obj['data'] = clean_model_dict(res)
        return HttpResponse(json.dumps(json_obj), content_type='application/json')
    else:
        if 'name' in request.GET and 'time' in request.GET:
            try:
                g_time = format_time(request.GET.get('time'))
            except Exception:
                error = {'error': 'Time format: Y-m-d H:M:S. %s doesn\'t fit.' % request.GET.get('time')}
                return HttpResponse(json.dumps(error), content_type='application/json')
            query = Q(platform__name=request.GET.get('name'))
            query &= Q(start_time__lte=g_time) & (Q(end_time__gte=g_time) | Q(end_time=None))
            res = PlatformDeployment.objects.filter(query)
            json_obj = {}
            json_obj['data'] = clean_model_dict(res)
            return HttpResponse(json.dumps(json_obj), content_type='application/json')

        elif 'name' in request.GET:
            res = PlatformDeployment.objects.filter(platform__name=request.GET.get('name'))
            json_obj = {}
            json_obj['data'] = clean_model_dict(res)
            return HttpResponse(json.dumps(json_obj), content_type='application/json')
        elif 'number' in request.GET:
            res = PlatformDeployment.objects.filter(deployment_number=request.GET.get('number'))
            json_obj = {}
            json_obj['data'] = clean_model_dict(res)
            return HttpResponse(json.dumps(json_obj), content_type='application/json')
        else:
            error = {'error': '\'name\' keyword not found'}
            return HttpResponse(json.dumps(error), content_type='application/json')


def get_deployment_instruments(request):
    Instrument = apps.get_model('instruments', 'Instrument')
    InstrumentOnPlatform = apps.get_model('instruments', 'InstrumentOnPlatform')
    if 'name' in request.GET and 'time' in request.GET:
        try:
            g_time = format_time(request.GET.get('time'))
        except Exception:
            error = {'error': 'Time format: Y-m-d H:M:S. %s doesn\'t fit.' % request.GET.get('time')}
            return HttpResponse(json.dumps(error), content_type='application/json')
        query = Q(platform__name=request.GET.get('name'))
        query &= Q(start_time__lte=g_time) & (Q(end_time__gte=g_time) | Q(end_time=None))
        res = InstrumentOnPlatform.objects.filter(query)
        print "he"
        print res
        json_obj = {}
        json_obj['data'] = clean_model_dict(res)
        return HttpResponse(json.dumps(json_obj), content_type='application/json')
    else:
        error = {'error': 'Both \'name\' and \'time\' are required.'}
        return HttpResponse(json.dumps(error), content_type='application/json')


def get_output_sensors(request):
    Sensor = apps.get_model('instruments', 'Sensor')
    if len(request.GET) == 0:
        res = Sensor.objects.all()
    else:
        gets = {
            'include_in_output': True
        }
        if 'id' in request.GET and 'name' not in request.GET:
            gets['instrument__id'] = request.GET.get('id')
            res = Sensor.objects.filter(**gets)
        elif 'identifier' in request.GET and 'id' not in request.GET:
            gets['instrument__identifier'] = request.GET.get('identifier')
            res = Sensor.objects.filter(**gets)
        else:
            error = {'error': 'Either \'id\' or \'identifier\' for platform are required.'}
            return HttpResponse(json.dumps(error), content_type='application/json')
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


def spec(request):
    pass


# Helpers
def convert_times(obj):
    for k in obj:
        if type(obj[k]) == datetime.datetime:
            obj[k] = obj[k].strftime('%Y-%m-%d %H:%M:%S')


def clean_model_dict(models):
    data = []
    print models
    for m in models:
        m_dict = copy.deepcopy(m.__dict__)
        del m_dict['_state']
        keys = m_dict.keys()
        to_add = []
        for key in keys:
            if 'id' in key and key != 'wmo_id':
                if key != 'id':
                    to_add.append(key.replace('_id', ''))
        for add in to_add:
            try:
                m_dict[add] = copy.deepcopy(getattr(m, add).__dict__)
                convert_times(m_dict[add])
                del m_dict[add]['_state']
            except AttributeError:
                pass  # It's a false alarm
        convert_times(m_dict)
        data.append(m_dict)
    return data


def format_time(t):
    return datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
