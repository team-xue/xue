# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class UniApplyApp(CMSApp):
    name = u'申请框架'
    urls = ['xue.uniapply.urls', ]
    # menu = []

apphook_pool.register(UniApplyApp)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
