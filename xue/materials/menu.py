# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from functools import partial

from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from xue.materials.models import MaterialEntry

HOME_ID, LIST_ID, ADD_ID = 1, 2, 3

ITEM_ID_BASE = 4


def do_append_node(lst, *args, **kwargs):
    return lst.append(NavigationNode(*args, **kwargs))


class CountingID(object):
    def __init__(self, initial=0):
        self.counter = initial

    def get(self):
        # XXX NOT THREAD-SAFE IF CLASS INSTANCE IS SHARED!!
        tmp = self.counter
        self.counter += 1
        return tmp


class MaterialsMenu(CMSAttachMenu):
    name = '材料中心菜单'

    def init_cache(self):
        cache = self.__urlcache = {}
        cache['home'] = reverse('xue.materials.views.homepage_view')
        cache['list'] = reverse('xue.materials.views.list_mine_view')
        cache['add'] = reverse('xue.materials.views.add_view')

    def get_nodes(self, request):
        try:
            self.__urlcache
        except AttributeError:
            # cache not initialized, do it now
            # it CANNOT be done in the ctor, since at that time the URLconf
            # is not loaded yet
            self.init_cache()

        usr, nodes, urlcache = request.user, [], self.__urlcache
        append = partial(do_append_node, nodes)
        counter = CountingID(ITEM_ID_BASE)
        new_id = counter.get

        append('起始页', urlcache['home'], HOME_ID)
        append('材料列表', urlcache['list'], LIST_ID)
        append('新建材料', urlcache['add'], ADD_ID)

        if usr.is_anonymous():
            # cannot continue, because the filter WILL fail!!
            return nodes

        for entry in MaterialEntry.objects.filter(user=usr):
            # the menu tree consists of NavigationNode instances
            # Each NavigationNode takes a label as first argument, a URL as
            # second argument and a (for this tree) unique id as third
            # argument.
            entry_id = new_id()
            append(
                    entry.title,
                    reverse(
                        'xue.materials.views.detail_view',
                        args=(entry.pk, ),
                        ),
                    entry_id,
                    LIST_ID,
                    )
            append(
                    '编辑',
                    reverse(
                        'xue.materials.views.edit_view',
                        args=(entry.pk, ),
                        ),
                    new_id(),
                    entry_id,
                    )

        return nodes


menu_pool.register_menu(MaterialsMenu)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
