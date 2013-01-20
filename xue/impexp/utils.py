# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

__all__ = [
        'render_model',
        ]

from django.http import HttpResponse
from django.template import Template, RequestContext

from django.utils.translation import ugettext_lazy as _u
_ = lambda x: x

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from .models import ExportTemplate

_get_for_model = ContentType.objects.get_for_model
_get_template = ExportTemplate.objects.get


def _get_template_model_for(obj, identifier):
    obj_type = _get_for_model(obj)
    return  _get_template(
            content_type__pk=obj_type.id,
            identifier=identifier,
            )


def get_template_for(obj, identifier):
    if type(identifier) in (str, unicode, ):
        # ident is template ID
        template_entry = _get_template_model_for(obj, identifier)
    else:
        # ident is _the_ desired object
        template_entry = identifier

    template_file = template_entry.template

    template_file.open('rb')
    try:
        template = template_file.read().decode('utf-8', 'ignore')
    finally:
        template_file.close()

    return Template(template)


def render_object(req, obj, ident, aggregate=False, ctx=None):
    tmpl_obj = get_template_for(obj, ident)
    ctx_dict = {} if ctx is None else ctx
    ctx_dict['e'] = obj
    ctx_dict['x_Agg'] = aggregate

    real_ctx = RequestContext(req, ctx_dict)
    return tmpl_obj.render(real_ctx)


def render_object_to_response(req, obj, ident, aggregate=False, ctx=None):
    return HttpResponse(render_object(req, obj, ident, aggregate, ctx))


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
