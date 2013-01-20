# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

__all__ = [
        'is_locked',
        'get_lock_status',
        'set_lock_status',
        ]

from django.utils.translation import ugettext_lazy as _u
_ = lambda x: x

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from .models import LockedStatus

_get_for_model = ContentType.objects.get_for_model
_status_get = LockedStatus.objects.get


def get_status_object_for(obj):
    obj_type = _get_for_model(obj)
    return  _status_get(
            content_type__pk=obj_type.id,
            object_id=obj.id,
            )


def get_lock_status(obj):
    try:
        stat = get_status_object_for(obj)
    except LockedStatus.DoesNotExist:
        return False, ''

    return stat.status, stat.reason


def is_locked(obj):
    stat, reason = get_lock_status(obj)
    return stat


def set_lock_status(obj, status, reason=None):
    try:
        stat = get_status_object_for(obj)
    except LockedStatus.DoesNotExist:
        stat = LockedStatus(rel_object=obj)

    if reason is not None:
        stat.status, stat.reason = status, reason
    else:
        stat.status = status

    stat.save()


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
