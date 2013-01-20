# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.shortcuts import redirect, get_object_or_404
from django.db import transaction

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from xue.common.decorators import quickview

from cms.models.tagmodel import Tag


@quickview('tagfrontend/index.html')
def tag_list_view(request):
    return {
            'tags': Tag.objects.all(),
            }


@quickview('section-tag.html')
def tag_view(request, tag_id):
    # this depends on menu subsystem to provide functionality...
    # but we still don't want non-existent tags to return success
    #
    # Tag is not Page, so theoretically section.html cannot be used for
    # displaying the list. After the employment of the cache machinery,
    # the "section" pages were completely broken because of non-existent
    # "current_page". section-tag.html was created to circumvent that.
    tag = get_object_or_404(Tag, pk=tag_id)

    return {
            'tag': tag,
            }



# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
