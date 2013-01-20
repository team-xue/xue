# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from accounts.menu import DMAccountMenu


class AccountsApp(CMSApp):
    name = _("Accounts")
    urls = ["accounts.urls", ]
    menu = [DMAccountMenu, ]

apphook_pool.register(AccountsApp)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
