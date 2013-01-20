# -*- coding: utf-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class TutorApp(CMSApp):
    name = u'导师申请' # give your app a name, this is required
    urls = ['xue.tutor.urls'] # link your app to url configuration(s)
    # menu = []

apphook_pool.register(TutorApp) # register your app


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
