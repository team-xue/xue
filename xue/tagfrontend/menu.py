# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from cms.menu_bases import CMSAttachMenu
from menus.base import Menu, NavigationNode
from menus.menu_pool import menu_pool
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.conf import settings

from cms.models.tagmodel import Tag
from cms.menu import page_to_node
from cms.utils import get_language_from_request
from cms.utils.moderator import get_page_queryset

# force preloading of url patterns... does this help?
from . import urls

from .views import tag_view


class CountingID(object):
    def __init__(self, initial=0):
        self.counter = initial

    def get(self):
        # XXX NOT THREAD-SAFE IF CLASS INSTANCE IS SHARED!!
        tmp = self.counter
        self.counter += 1
        return tmp


class TagMenu(CMSAttachMenu):
    name = '标签菜单'

    def get_nodes(self, request):
        usr, nodes = request.user, []

        # much of this init code is the same as cms/menu.py to ensure
        # result compatibility
        # don't need to pass in request, since the tag app is only here
        # to help organize articles, not assist in moderation flow.
        page_queryset = get_page_queryset()
        site = Site.objects.get_current()
        lang = get_language_from_request(request)
        filters = {
            'site': site,
        }
        if settings.CMS_HIDE_UNTRANSLATED:
            filters['title_set__language'] = lang
        pages = page_queryset.published().filter(**filters).order_by(
                '-creation_date',
                #"tree_id",
                #"lft",
                )

        # menu-building helper vars
        append = nodes.append
        counter = CountingID(1)
        new_id = counter.get

        # Create nodes for tags and related pages in one pass
        for tag in Tag.objects.all():
            # 1. node for tag
            node_id = new_id()
            append(NavigationNode(
                tag.name,
                reverse(
                    'xue.tagfrontend.views.tag_view',
                    args=(tag.pk, ),
                    ),
                node_id,
                # make the pages referrable from CMS templates!
                attr={
                    'reverse_id': 'cmstag_%s' % tag.name,
                    },
                ))

            # 2. related pages
            # we'll reuse CMS's page_to_node but modify the
            # result node slightly
            for page in pages.filter(tags=tag):
                # get the node as it's returned by the CMS
                # TODO: is the simplified params appropriate?
                page_node = page_to_node(page, page, False)

                # modify it to fit in our tree structure
                page_node.id = new_id()
                page_node.parent_id = node_id
                append(page_node)

        return nodes


menu_pool.register_menu(TagMenu)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
