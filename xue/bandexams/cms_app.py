# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class BandexamsApp(CMSApp):
    name = u'等级考试'
    urls = ['xue.bandexams.urls', ]
    # menu = []

apphook_pool.register(BandexamsApp)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
