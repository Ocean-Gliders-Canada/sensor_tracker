import copy
import datetime
import re

from django.conf import settings
from django.apps import apps
from functools import lru_cache


@lru_cache(maxsize=None)
def get_apps_model_name():
    all_models = []
    for name in settings.LOCAL_APPS:
        app_models = apps.get_app_config(name).get_models()
        all_models.extend(app_models)
    all_models_names = []
    if all_models:
        for m in all_models:
            word_list = re.findall('[A-Z][^A-Z]*', m.__name__)

            res = '_'.join(word_list)
            all_models_names.append(res.lower())
    return all_models_names


@lru_cache(maxsize=None)
def get_all_model_id_name():
    all_model_id = []
    for n in get_apps_model_name():
        all_model_id.append(n + '_id')
    all_model_id.append('master_instrument_id')
    all_model_id.append('user_id')
    all_model_id.append('power_type_id')
    return all_model_id


def get_name(model):
    the_list = ['name', 'identifier', 'model', 'username']
    name = None
    for n in the_list:
        try:
            name = getattr(model, n)
            break
        except AttributeError:
            pass
    return name


def convert_times(obj):
    """Convert Datetime into str"""
    if type(obj) == dict:
        for k in obj:
            if type(obj[k]) == datetime.datetime:
                obj[k] = obj[k].strftime('%Y-%m-%d %H:%M:%S')


def convert_model_to_dict_simple(model):
    """Convert object into dict, no recursive convert"""
    m_dict = copy.deepcopy(model.__dict__)
    try:
        del m_dict['_state']
        del m_dict['id']
    except KeyError as e:
        print("keyerror {}".format(e))
    to_add_id_key = []
    for id_key in get_all_model_id_name():
        if id_key in m_dict:
            del m_dict[id_key]
            to_add_id_key.append(id_key)
    for k in to_add_id_key:
        k = k[:-3]
        o = getattr(model, k)
        if o:
            the_name = get_name(o)
            if the_name:
                m_dict[k] = the_name
        else:
            m_dict[k] = None
    convert_times(m_dict)
    return m_dict


def convert_model_to_dict_recursive(model):
    """convert model to dict recursively"""
    m_dict = copy.deepcopy(model.__dict__)
    del m_dict['_state']
    del m_dict['id']
    to_add_id_key = []
    for id_key in get_all_model_id_name():
        if id_key in m_dict:
            del m_dict[id_key]
            to_add_id_key.append(id_key)
    for k in to_add_id_key:
        k = k[:-3]
        o = getattr(model, k)
        if o:
            m_dict[k] = convert_model_to_dict_recursive(o)
        else:
            m_dict[k] = None
    convert_times(m_dict)
    return m_dict
