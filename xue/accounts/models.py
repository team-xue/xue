# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from userena.models import UserenaLanguageBaseProfile
from django.utils.translation import ugettext_lazy as _

from xue.common.choices import *
from xue.classes.models import LogicalClass


class DMUserProfile(UserenaLanguageBaseProfile):
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='profile')
    realname = models.CharField('真实姓名', max_length=32)
    gender = models.IntegerField('性别', choices=GENDER_CHOICES, default=0)
    id_number = models.CharField('标识号', max_length=20)
    role = models.IntegerField('身份', choices=ROLE_CHOICES, null=True)

    nickname = models.CharField(
            '昵称',
            max_length=32,
            blank=True,
            default='',
            )

    sign_line = models.CharField(
            '个性签名',
            max_length=128,
            blank=True,
            default='',
            )

    def __unicode__(self):
        return '用户资料: %s (%s) [%s]' % (
                self.realname,
                self.user.username,
                ROLE_DICT.get(self.role, '未知角色'),
                )


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
