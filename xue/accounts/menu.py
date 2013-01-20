# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from menus.base import NavigationNode
from cms.menu_bases import CMSAttachMenu
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _


class DMAccountMenu(CMSAttachMenu):
    name = _('Accounts')

    def get_nodes(self, request):
        nodes = []

        def _add_node(*args, **kwargs):
            nodes.append(NavigationNode(*args, **kwargs))

        _add_node(_('Details'), "/", 1)
        _add_node(_('Login'), "/signin/", 2)
        _add_node(_('Register'), "/signup/", 3)
        _add_node(_('Logout'), "/signout/", 4)

        return nodes


menu_pool.register_menu(DMAccountMenu)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
