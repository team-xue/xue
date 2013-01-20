# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from .menu import TagMenu


class TagApp(CMSApp):
    name = _("Tag frontend")
    urls = ["xue.tagfrontend.urls", ]
    menu = [TagMenu, ]


apphook_pool.register(TagApp)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
