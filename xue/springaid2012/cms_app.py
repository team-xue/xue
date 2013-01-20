# -*- coding: utf-8 -*-

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

# from accounts.menu import DMAccountMenu

class SpringAid2012App(CMSApp):
    name = u'春季国家助学金 2012' # give your app a name, this is required
    urls = ['springaid2012.urls'] # link your app to url configuration(s)
    # menu = [DMAccountMenu]

apphook_pool.register(SpringAid2012App) # register your app


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
