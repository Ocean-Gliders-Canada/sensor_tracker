from django.urls import reverse, get_script_prefix, get_resolver, get_urlconf
from django.db.models import Q


def make_edit_link(instance):
    opt = instance._meta
    link = reverse('admin:{}_{}_change'.format(opt.app_label, opt.model_name), args=(instance.id,))
    return link


def make_add_link(instance):
    opt = instance._meta
    link = reverse('admin:{}_{}_add'.format(opt.app_label, opt.model_name))
    print("script_prefix", get_script_prefix())
    return link


def qs_time_overlap(base_qs, start_time, end_time):
    if end_time:
        soi_qs_overlap = base_qs.filter(
            Q(start_time__lte=start_time, end_time__gte=start_time) | Q(start_time__lte=end_time,
                                                                        end_time__gte=end_time))
    else:
        soi_qs_overlap = base_qs.filter(Q(end_time=None) | Q(start_time__lte=start_time))

    return soi_qs_overlap
