# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from xue.materials.menu import MaterialsMenu


class MaterialsApp(CMSApp):
    name = '材料中心'
    urls = ['xue.materials.urls', ]
    menu = [MaterialsMenu, ]


apphook_pool.register(MaterialsApp)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
