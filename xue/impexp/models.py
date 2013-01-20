# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from django.db import models
from django.utils.translation import ugettext_lazy as _u
_ = lambda x: x

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


class ExportTemplate(models.Model):
    class Meta:
        verbose_name = '导出用模板'
        verbose_name_plural = '导出用模板'

    content_type = models.ForeignKey(
            ContentType,
            verbose_name=_('关联模型'),
            )

    title = models.CharField(_('模板标题'), max_length=255)

    identifier = models.CharField(
            _('内部名称'),
            max_length=128,
            unique=True,
            )

    # TODO: caching
    template = models.FileField(
            upload_to='impexp/exports/%Y%m/',
            verbose_name=_('模板文件'),
            )

    def __unicode__(self):
        return '[导出用模版 %s]' % (
                self.title,
                # unicode(self.content_type),
                )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
