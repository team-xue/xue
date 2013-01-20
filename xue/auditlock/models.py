# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from django.db import models
from django.utils.translation import ugettext_lazy as _u
_ = lambda x: x

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class LockedStatus(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    rel_object = generic.GenericForeignKey('content_type', 'object_id')

    status = models.BooleanField(_('已锁定'), default=False)
    reason = models.CharField(_('锁定原因'), max_length=255, blank=True)

    class Meta:
        # this is an one-to-one thing
        unique_together = (
                ('content_type', 'object_id', ),
                )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
