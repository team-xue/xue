# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from functools import wraps
from django.template import RequestContext
from django.shortcuts import render_to_response


def quickview(template_name, **kwargs):
    def _decorator_(fn):
        @wraps(fn)
        def _wrapped_(request, *args1, **kwargs1):
            ret_dict = fn(request, *args1, **kwargs1)
            if type(ret_dict) is not dict:
                return ret_dict
            ret_dict.update(kwargs)
            return render_to_response(template_name,
                    ret_dict,
                    context_instance=RequestContext(request))
        return _wrapped_
    return _decorator_


def _is_role_legitimate(user, accepted_roles, denied_roles):
    if user.is_anonymous():
        return False

    if user.is_superuser:
        # superuser is THE super user, after all...
        return True

    try:
        profile = user.profile
    except AttributeError:
        # no associated profile? weird...
        return False

    role = profile.role
    if role in denied_roles:
        # DENY rules come first
        return False

    if role not in accepted_roles:
        return False

    return True


def limit_role(accepted_roles, denied_roles=None):
    if denied_roles is None:
        denied_roles = []

    def _decorator_(fn):
        @wraps(fn)
        def _wrapped_(request, *args, **kwargs):
            usr = request.user
            if not _is_role_legitimate(usr, accepted_roles, denied_roles):
                # role mismatch, give 403
                response = render_to_response(
                        '403.html',
                        {'reason': '您的角色不能进行此操作', },
                        context_instance=RequestContext(request),
                        )
                # "simulate" a HttpResponseForbidden
                response.status_code = 403
                return response
            # role match
            return fn(request, *args, **kwargs)
        return _wrapped_
    return _decorator_


def debuglog(logname):
    def _do_debuglog(fn):
        @wraps(fn)
        def __wrapped__(*args, **kwargs):
            with open(logname, 'a+') as fp:
                print >>fp, u'CALL: %s\n    args: %s\n    kwargs: %s' % (
                        fn.func_name,
                        unicode(args),
                        unicode(kwargs),
                        )
                result = fn(*args, **kwargs)
                print >>fp, u'    result: %s\n' % unicode(result)
            return result
        return __wrapped__
    return _do_debug


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8:
