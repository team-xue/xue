# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _u
_ = lambda x: x

from ..common.choices import *


class BandExamResult(models.Model):
    class Meta:
        verbose_name = _('等级考试成绩')
        verbose_name_plural = _('等级考试成绩')

    user = models.ForeignKey(
            User,
            verbose_name=_u('user'),
            )
    exam_type = models.IntegerField(
            _('等级考试类型'),
            choices=BAND_CHOICES,
            )
    score = models.IntegerField(
            _('考试成绩'),
            default=0,
            )

    def __unicode__(self):
        return '%(name)s 的 %(exam)s (%(score)d 分)' % {
                'name': self.get_realname,
                'exam': BAND_DICT.get(self.exam_type, '[未知]'),
                'score': self.score,
                }

    def get_realname(self):
        return user.profile.realname
    get_realname.short_description = _('真实姓名')


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
