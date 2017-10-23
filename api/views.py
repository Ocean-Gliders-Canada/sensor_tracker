# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy
import json
import datetime

from django.apps import apps
from django.core import serializers
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

import specs


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


@api_view(['GET'])
def get_instruments(request):
    Instrument = apps.get_model('instruments', 'Instrument')

    if len(request.GET) == 0:
        res = Instrument.objects.all()
    else:
        gets = {}
        if 'id' in request.GET and 'identifier' in request.GET:
            return error_result('Either include \'id\' or \'identifier\', not both.')
        elif 'id' in request.GET:
            gets['id'] = request.GET.get('id')
        elif 'identifier' in request.GET:
            gets['identifier'] = request.GET.get('identifier')
        res = Instrument.objects.filter(**gets)
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


@api_view(['GET'])
def get_instruments_on_platform(request):
    InstrumentOnPlatform = apps.get_model('instruments', 'InstrumentOnPlatform')

    if len(request.GET) == 0:
        res = InstrumentOnPlatform.objects.all()
    else:
        query = None
        if 'id' in request.GET and ('name' in request.GET or 'time' in request.GET or 'identifier' in request.GET):
            return error_result('If \'id\' is included, it must be the only argument.')
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


@api_view(['GET'])
def get_sensors(request):
    Sensor = apps.get_model('instruments', 'Sensor')
    if len(request.GET) == 0:
        res = Sensor.objects.all()
    else:
        gets = {}

        if 'id' in request.GET and 'identifier' in request.GET:
            return error_result('Either include \'id\' or \'identifier\', not both.')
        elif 'id' in request.GET:
            gets['id'] = request.GET.get('id')
        if 'identifier' in request.GET:
            gets['identifier'] = request.GET.get('identifier')
        res = Sensor.objects.filter(**gets)
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


@api_view(['GET'])
def get_platform(request):
    Platform = apps.get_model('platforms', 'Platform')
    if len(request.GET) == 0:
        res = Platform.objects.all()
    else:
        gets = {}
        if 'id' in request.GET and 'name' in request.GET:
            return error_result('Either include \'id\' or \'name\', not both.')
        elif 'id' in request.GET:
            gets['id'] = request.GET.get('id')
        elif 'name' in request.GET:
            gets['name'] = request.GET.get('name')
        res = Platform.objects.filter(**gets)
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


@api_view(['GET'])
def get_manufacturer(request):
    Manufacturer = apps.get_model('general', 'Manufacturer')
    if len(request.GET) == 0:
        res = Manufacturer.objects.all()
    else:
        gets = {}
        if 'id' in request.GET and 'name' in request.GET:
            return error_result('Either include \'id\' or \'name\', not both.')
        elif 'id' in request.GET:
            gets['id'] = request.GET.get('id')
        elif 'name' in request.GET:
            gets['name'] = request.GET.get('name')
        res = Manufacturer.objects.filter(**gets)
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


@api_view(['GET'])
def get_institutions(request):
    Institution = apps.get_model('general', 'Institution')
    if len(request.GET) == 0:
        res = Institution.objects.all()
    else:
        gets = {}
        if 'id' in request.GET and 'name' in request.GET:
            return error_result('Either include \'id\' or \'name\', not both.')
        elif 'id' in request.GET:
            gets['id'] = request.GET.get('id')
        elif 'name' in request.GET:
            gets['name'] = request.GET.get('name')
        res = Institution.objects.filter(**gets)
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


@api_view(['GET'])
def get_project(request):
    Project = apps.get_model('general', 'Project')
    if len(request.GET) == 0:
        res = Project.objects.all()
    else:
        gets = {}
        if 'id' in request.GET and 'name' in request.GET:
            return error_result('Either include \'id\' or \'name\', not both.')
        if 'id' in request.GET:
            gets['id'] = request.GET.get('id')
        if 'name' in request.GET:
            gets['name'] = request.GET.get('name')
        res = Project.objects.filter(**gets)
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


@api_view(['GET'])
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


@api_view(['GET'])
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
            return error_result('No valid arguments found.')


@api_view(['GET'])
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
        json_obj = {}
        json_obj['data'] = clean_model_dict(res)
        return HttpResponse(json.dumps(json_obj), content_type='application/json')
    else:
        error = {'error': 'Both \'name\' and \'time\' are required.'}
        return HttpResponse(json.dumps(error), content_type='application/json')


@api_view(['GET'])
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


# POST Requests

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_deployment(request):
    Deployment = apps.get_model('platforms', 'PlatformDeployment')
    deployment = create_object_from_request(request, Deployment)

    return save_and_result(deployment)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_platform(request):
    Platform = apps.get_model('platforms', 'Platform')
    platform = create_object_from_request(request, Platform)

    return save_and_result(platform)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_project(request):
    Project = apps.get_model('general', 'Project')
    project = create_object_from_request(request, Project)

    return save_and_result(project)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_instrument_on_platform(request):
    InstrumentOnPlatform = apps.get_model('instruments', 'InstrumentOnPlatform')
    instrument_on_platform = create_object_from_request(request, InstrumentOnPlatform)

    return save_and_result(instrument_on_platform)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_platform_type(request):
    PlatformType = apps.get_model('platforms', 'PlatformType')
    platform_type = create_object_from_request(request, PlatformType)

    return save_and_result(platform_type)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_instrument(request):
    Instrument = apps.get_model('instruments', 'Instrument')
    instrument = create_object_from_request(request, Instrument)

    return save_and_result(instrument)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_sensor(request):
    Sensor = apps.get_model('instruments', 'Sensor')
    sensor = create_object_from_request(request, Sensor)

    return save_and_result(sensor)


def spec(request):
    template = loader.get_template('spec.html')
    context = {
        'urls': specs.specs,
        'links': specs.links
    }
    return HttpResponse(template.render(context, request))


# Helpers
def create_object_from_request(request, Object, time_columns=['start_time', 'end_time']):
    fields = [x.get_attname_column()[0] for x in Object._meta.fields]
    kargs = {}
    for field in fields:
        print field
        if field in request.POST:
            if field in time_columns:
                kargs[field] = datetime.datetime.strptime(request.POST.get(field), '%Y-%m-%d %H:%M:%S')
            else:
                kargs[field] = request.POST.get(field)
    print kargs
    return Object(**kargs)


def save_and_result(model):
    try:
        model.save()
        res = {
            'success': True,
            'id': model.id
        }
        return HttpResponse(json.dumps(res), content_type='application/json')
    except IntegrityError as e:
        return error_result(e.message.replace('DETAIL', '').strip())


def error_result(error):
    res = {'error': error}
    return HttpResponse(json.dumps(res), content_type='application/json')


def convert_times(obj):
    if type(obj) == dict:
        for k in obj:
            if type(obj[k]) == datetime.datetime:
                obj[k] = obj[k].strftime('%Y-%m-%d %H:%M:%S')


def clean_model_dict(models, no_foreign=['wmo_id']):
    data = []
    print models
    for m in models:
        m_dict = copy.deepcopy(m.__dict__)
        del m_dict['_state']
        keys = m_dict.keys()
        to_add = []
        for key in keys:
            if 'id' in key and key not in no_foreign:
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
