# -*- coding: utf-8 -*-
import copy
import json
import datetime

from django.apps import apps
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from api import specs


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
        if 'id' in request.GET and ('identifier' in request.GET or 'serial' in request.GET):
            return error_result('\'id\' must be the only arg if \'id\' is used.')
        elif 'id' in request.GET:
            gets['id'] = request.GET.get('id')
        else:
            if 'identifier' in request.GET:
                gets['identifier'] = request.GET.get('identifier')
            if 'serial' in request.GET:
                gets['serial'] = request.GET.get('serial')
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
def get_sensors(request):
    Sensor = apps.get_model('instruments', 'Sensor')
    if len(request.GET) == 0:
        res = Sensor.objects.all()
    else:
        gets = {}
        if 'id' in request.GET and 'identifier' not in request.GET and 'instrument_id' not in request.GET:
            gets['id'] = request.GET.get('id')
        elif 'identifier' in request.GET and 'id' not in request.GET and 'instrument_id' not in request.GET:
            gets['identifier'] = request.GET.get('identifier')
        elif 'instrument_id' in request.GET and 'id' not in request.GET and 'identifier' not in request.GET:
            gets['instrument_id'] = request.GET.get('instrument_id')
        elif 'instrument_id' in request.GET and 'identifier' in request.GET and 'id' not in request.GET:
            gets['identifier'] = request.GET.get('identifier')
            gets['instrument_id'] = request.GET.get('instrument_id')
        else:
            return error_result('Invalid arguments')
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
        elif 'type' in request.GET:
            gets['platform_type__model'] = request.GET.get('type')
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
def get_platform_by_type(request):
    PlatformType = apps.get_model('platforms', 'PlatformType')
    Platform = apps.get_model('platforms', 'Platform')
    if len(request.GET) == 0:
        res = PlatformType.objects.all()
    else:
        if 'model' in request.GET:
            model = request.GET.get('model')
            platform_type = PlatformType.objects.filter(model=model)
            res = Platform.objects.filter(platform_type=platform_type)
        else:
            error = {'error': 'Must choose either model or platform name to search by, not both.'}
            return HttpResponse(json.dumps(error), content_type='application/json')
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
        print(request.GET)
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
        elif 'deployment_number' in request.GET:
            res = PlatformDeployment.objects.filter(deployment_number=request.GET.get('deployment_number'))
            json_obj = {}
            json_obj['data'] = clean_model_dict(res)
            return HttpResponse(json.dumps(json_obj), content_type='application/json')
        else:
            return error_result('No valid arguments found.')


@api_view(['GET'])
def get_platform_deployment_comments(request):
    PlatformDeploymentComment = apps.get_model('platforms', 'PlatformDeploymentComment')
    PlatformDeployment = apps.get_model('platforms', 'PlatformDeployment')

    if (request.GET) == 0:
        res = PlatformDeploymentComment.objects.all()
    else:
        if "name" in request.GET and "time" in request.GET:
            try:
                g_time = format_time(request.GET.get('time'))
            except Exception:
                error = {'error': 'Time format: Y-m-d H:M:S. %s doesn\'t fit.' % request.GET.get('time')}
                return HttpResponse(json.dumps(error), content_type='application/json')
            query = Q(platform__name=request.GET.get('name'))
            query &= Q(start_time__lte=g_time) & (Q(end_time__gte=g_time) | Q(end_time=None))
            res = PlatformDeployment.objects.filter(query)
            PlatformDeploymentId = res[0].id
            print(PlatformDeploymentId)
            query = Q(platform_deployment_comment_box__platform_deployment=res)
            res = PlatformDeploymentComment.objects.filter(query)
        else:
            return error_result('No valid arguments found.')
    json_obj = {}
    json_obj['data'] = clean_model_dict(res)
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


@api_view(['GET'])
def get_output_sensors(request):
    Sensor = apps.get_model('instruments', 'Sensor')
    gets = {
        'include_in_output': True
    }
    if len(request.GET) == 0:
        res = Sensor.objects.filter(**gets)
    else:
        if 'id' in request.GET and 'identifier' not in request.GET:
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


@api_view(['GET'])
def get_most_recent_deployment(request):
    PlatformDeployment = apps.get_model('platforms', 'PlatformDeployment')
    gets = {}
    if 'id' in request.GET and 'name' not in request.GET:
        gets['platform__id'] = request.GET.get('id')
    elif 'id' not in request.GET and 'name' in request.GET:
        gets['platform__name'] = request.GET.get('name')
    else:
        return error_result('Either \'id\' or \'name\' of a platform is required.')
    res = PlatformDeployment.objects.filter(**gets).order_by('-start_time')
    json_obj = {
        'data': clean_model_dict(res)[0]
    }
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


@api_view(['GET'])
def get_power(request):
    PlatformDeployment = apps.get_model('platforms', 'PlatformPowerType')
    id = None
    name = None
    if "name" in request.GET:
        name = request.GET.get('name')
    else:
        return error_result('name of battery is required.')
    res = PlatformDeployment.objects.filter(name=name)
    json_obj = {
        'data': clean_model_dict(res)[0]
    }
    return HttpResponse(json.dumps(json_obj), content_type='application/json')


# POST Requests

@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def insert_deployment(request):
    Deployment = apps.get_model('platforms', 'PlatformDeployment')
    types = {"wmo_id": int, "deployment_number": int, "platform_id": int, "institution_id": int, "project_id": int,
             "power_type_id": int, "platform_name": str, "title": str, "start_time": str, "end_time": str,
             "testing_mission": bool, "comment": str, "acknowledgement": str,
             "contributor_name": str, "contributor_role": str, "creator_email": str, "creator_name": str,
             "creator_url": str, "data_repository_link": str, "publisher_email": str, "publisher_name": str,
             "publisher_url": str, "metadata_link": str, "references": str, "sea_name": str,
             "latitude": float, "longitude": float, "depth": float}
    deployment = create_object_from_request(request, Deployment, value_type=types)

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


@api_view(['POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def update_component(request):
    lookup = {
        'deployment': ('platforms', 'PlatformDeployment'),
        'platform': ('platforms', 'Platform'),
        'project': ('general', 'Project'),
        'instruments_platform': ('instruments', 'InstrumentOnPlatform'),
        'platform_type': ('platforms', 'PlatformType'),
        'instrument': ('instruments', 'Instrument'),
        'sensor': ('instruments', 'Sensor'),
    }
    if 'component' in request.POST and 'id' in request.POST:
        try:
            Component = apps.get_model(*lookup[request.POST.get('component')])
        except KeyError:
            err = "'%s' is not a component." % request.POST.get('component')
            return error_result(err)

        try:
            component = Component.objects.filter(id=request.POST.get('id'))
            if len(component) == 0:
                err = 'Could not find %s with that id.' % request.POST.get('component')
                return error_result(err)
            component = component.first()
        except ValueError:
            err = "'id' must be an integer."
            return error_result(err)
        fields = [x.get_attname_column()[0] for x in Component._meta.fields]
        fields.remove('id')
        for field in fields:
            if field in request.POST:
                setattr(component, field, request.POST.get(field))
        component.save()
        res = {
            'success': True,
            'message': 'Updated \'%s\' with id %s.' % (
                request.POST.get('component'),
                request.POST.get('id')
            )
        }
        return HttpResponse(json.dumps(res), content_type='application/json')


def spec(request):
    template = loader.get_template('spec.html')
    context = {
        'urls': specs.specs,
        'links': specs.links
    }
    return HttpResponse(template.render(context, request))


@permission_classes([IsAuthenticated])
def validate_token(request):
    res = {
        'success': True
    }
    return HttpResponse(json.dumps(res), content_type='application/json')


# Helpers
def create_object_from_request(request, object, time_columns=None, value_type=None):
    if time_columns is None:
        time_columns = ['start_time', 'end_time']
    fields = [x.get_attname_column()[0] for x in object._meta.fields]
    kargs = {}
    for field in fields:
        if field in request.POST:
            if field in time_columns:
                kargs[field] = datetime.datetime.strptime(request.POST.get(field), '%Y-%m-%d %H:%M:%S')
            else:
                kargs[field] = request.POST.get(field)
    if value_type is not None:
        kargs = check_input_type(kargs, value_type)
    return object(**kargs)


def check_input_type(content, value_type):
    new_content = {}
    for key in content:
        value = content[key]
        if key in value_type:
            t = value_type[key]
            try:
                new_item = t(value)
            except:
                new_item = None
            new_content[key] = new_item
    return new_content


def save_and_result(model):
    try:
        model.save()
        res = {
            'success': True,
            'id': model.id
        }
        return HttpResponse(json.dumps(res), content_type='application/json')
    except Exception as e:
        print(e)
        return error_result(e.message.replace('DETAIL', '').strip())


def error_result(error):
    res = {'success': False, 'error': error}
    return HttpResponse(json.dumps(res), content_type='application/json')


def convert_times(obj):
    if type(obj) == dict:
        for k in obj:
            if type(obj[k]) == datetime.datetime:
                obj[k] = obj[k].strftime('%Y-%m-%d %H:%M:%S')


def clean_model_dict(models, no_foreign=['wmo_id']):
    data = []
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
