#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This code is part of the xue project.

from __future__ import unicode_literals, division

from cgi import escape as htmlescape

from django import template
register = template.Library()

from xue.__version__ import VERSION_DEV, VERSION_STR

HAVE_UA_PARSER = False
try:
    from ua_parser import user_agent_parser
    HAVE_UA_PARSER = True
except ImportError:
    pass


def version_node_factory(s):
    ver = htmlescape(s if s else 'unknown')

    class _XueVersionNode(template.Node):
        def render(self, context):
            return ver

    return _XueVersionNode


XueDevVersionNode = version_node_factory(VERSION_DEV)
XueVersionNode = version_node_factory(VERSION_STR)


if HAVE_UA_PARSER:
    class XueUAStringNode(template.Node):
        def __init__(self):
            pass

        def render(self, context):
            # protect against UA-less requests
            try:
                ua_string = context['request'].META['HTTP_USER_AGENT']
            except KeyError:
                return '[未知]'

            ua_dict = user_agent_parser.Parse(ua_string)
            dev, d_os, ua = (
                    ua_dict['device'],
                    ua_dict['os'],
                    ua_dict['user_agent'],
                    )

            result = []

            if dev.get('is_spider', False):
                result.append('[爬虫]')

            if dev.get('is_mobile', False):
                result.append('[便携]')
                if dev['family'] is not None:
                    result.append('[%s]' % dev['family'])

            os_family = d_os['family']
            os_maj, os_min = d_os['major'], d_os['minor']
            if os_family != 'Other':
                if os_family == 'Android':
                    result.append('[安卓')

                    if os_maj is not None:
                        result.append(unicode(os_maj))
                    if os_min is not None:
                        result.append('.%s' % (os_min, ))
                    result.append(']')
                else:
                    result.append('[%s]' % os_family)

            ua_family = ua['family']
            ua_version = [ua['major'], ua['minor'], ua['patch'], ]
            if ua_family != 'Other':
                result.append(' ')
                result.append(ua_family)
                result.append(' ')
                result.append('.'.join(unicode(i) for i in ua_version[:2]))
                if ua_version[2] is not None:
                    result.append('.%s' % (ua_version[2], ))

            result_str = u''.join(result)

            # I just want to fetch some info, so...
            ##request_uri = context['request'].META['REQUEST_URI']
            ##with open('D:\\UAStringNode-result.log', 'a+') as fp:
            ##    fp.write('%s: %s\n' % (
            ##            request_uri,
            ##            str(ua),
            ##            ))

            return htmlescape(result_str)
else:
    class XueUAStringNode(template.Node):
        def __init__(self):
            pass

        def render(self, context):
            return '<span class="error">ua-parser not available!</span>'


@register.tag
def xue_dev_version(parser, token):
    tokens = token.split_contents()
    if len(tokens) > 1:
        raise ValueError('%r tag requires no argument' % tokens[0])

    return XueDevVersionNode()


@register.tag
def xue_version(parser, token):
    tokens = token.split_contents()
    if len(tokens) > 1:
        raise ValueError('%r tag requires no argument' % tokens[0])

    return XueVersionNode()


@register.tag
def xue_uastring(parser, token):
    tokens = token.split_contents()
    if len(tokens) > 1:
        raise ValueError('%r tag requires no argument' % tokens[0])

    return XueUAStringNode()


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8:
