#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is part of the xue project.

from __future__ import unicode_literals, division

from cgi import escape as htmlescape

from django import template
register = template.Library()

from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

from ..choices import *
from ...bandexams.models import BandExamResult
from ...materials.models import MaterialEntry

from ...impexp.utils import render_object


@register.filter
def x_BandExamMax(value, arg):
    qs = BandExamResult.objects.filter(
            user=value,
            exam_type=int(arg),
            )

    if qs.exists():
        return unicode(max(i.score for i in qs))

    return ''


@register.filter
def x_RealName(value):
    try:
        return value.profile.realname
    except AttributeError:
        return 'ERROR!!'


@register.filter
def x_Birthday(value):
    try:
        birthday = value.central_info.birthday
        if birthday is None:
            return ''
    except AttributeError:
        return ''


@register.filter
def x_Gender(value):
    try:
        return GENDER_DICT.get(value.profile.gender, '??')
    except AttributeError:
        return '???'


@register.filter
def x_PoliticalBkgnd(value):
    try:
        return POLITICAL_BKGND_DICT.get(value.central_info.political, '??')
    except AttributeError:
        return '???'


@register.filter
def x_Ethnic(value):
    try:
        return ETHNIC_DICT.get(value.central_info.ethnic, '??')
    except AttributeError:
        return '???'


@register.filter
def x_uniEntryMaterialsTitled(value, name):
    qs = []
    try:
        qs = list(value.materials.filter(
                title__icontains=name,
                ))
    except ObjectDoesNotExist:
        pass

    return qs


@register.filter
def x_matFormatAsList(value, tagname):
    lines = value.content.splitlines()

    start_tag, end_tag = tagname.join(('<', '>')), tagname.join(('</', '>'))
    tags = (start_tag, end_tag, )

    # Must escape here as we're generating tags!
    result = (htmlescape(ln).join(tags) for ln in lines)
    return mark_safe('\n'.join(result))


@register.filter
def x_matParseAsIntList(value):
    lines = (ln.strip() for ln in value.content.splitlines())
    return [int(ln) for ln in lines if len(ln) > 0]


@register.filter
def x_numAvg(value):
    lst = list(value)
    return sum(lst) / len(lst)


@register.filter
def x_Idx(value, arg):
    try:
        idx = int(arg)
    except ValueError:
        return ''

    try:
        return value[idx]
    except IndexError:
        return ''


@register.filter
def x_RenderObjectsAgg(value, args):
    # one argument limitation...
    request, ident = args

    result = []
    last = len(value) - 1

    for idx, obj in enumerate(value):
        is_first, is_last = idx == 0, idx == last

        rendered = render_object(
                request,
                obj,
                ident,
                aggregate=True,
                ctx={
                    'x_First': is_first,
                    'x_Last': is_last,
                    },
                )

        result.append(rendered)

    return mark_safe('\n'.join(result))


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8:
