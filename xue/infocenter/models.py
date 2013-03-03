# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _u
_ = lambda x: x

from ..common.choices import *
from ..classes.models import LogicalClass

# Effective fields used in calculation of info completeness
# They are all CharField's
_EFF_FIELDS = (
        'location', 'postal',
        'ident', 'ident_pa', 'ident_ma',
        'name_pa', 'name_ma',
        'unit_pa', 'unit_ma',
        'phone', 'phone_family',
        'high_school', 'hobby',
        )
_EFF_FIELDS_COUNT = len(_EFF_FIELDS)


class CentralStudentInfo(models.Model):
    class Meta:
        verbose_name = _('学生信息')
        verbose_name_plural = _('学生信息')

    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_u('user'),
                                related_name='central_info')
    is_locked = models.BooleanField(_('已锁定'), default=False)

    klass = models.ForeignKey(LogicalClass, verbose_name=_('从属班级'), null=True)

    birthday = models.DateField(_('出生日期'), null=True)
    join_date = models.DateField(_('加入日期'), null=True)
    ethnic = models.IntegerField(
            _('民族'),
            choices=ETHNIC_CHOICES,
            default=0,  # Han Chinese
            )
    location = models.CharField(
            _('家庭住址'),
            max_length=256,
            blank=True,
            )
    postal = models.CharField(_('邮政编码'), max_length=6, blank=True)

    ident = models.CharField(_('身份证号码'), max_length=18, blank=True)
    ident_pa = models.CharField(_('父亲身份证号'), max_length=18, blank=True)
    ident_ma = models.CharField(_('母亲身份证号'), max_length=18, blank=True)

    name_pa = models.CharField(_('父亲姓名'), max_length=32, blank=True)
    name_ma = models.CharField(_('母亲姓名'), max_length=32, blank=True)
    unit_pa = models.CharField(_('父亲工作单位'), max_length=128, blank=True)
    unit_ma = models.CharField(_('母亲工作单位'), max_length=128, blank=True)

    phone = models.CharField(_('手机号码'), max_length=24, blank=True)
    phone_family = models.CharField(_('家庭电话'), max_length=24, blank=True)

    political = models.IntegerField(
            _('政治面貌'),
            choices=POLITICAL_BKGND_CHOICES,
            default=0,
            )
    cylc_date = models.DateField(
            _('入团时间'),
            blank=True,
            null=True,
            )
    cpc_date = models.DateField(
            _('入党时间'),
            blank=True,
            null=True,
            )


    railway_station = models.CharField(
            _('乘火车区间'),
            max_length=16,
            blank=True,
            )

    high_school = models.CharField(
            _('高中学校'),
            max_length=32,
            blank=True,
            default='',
            )

    english_band_type = models.IntegerField(
            _('英语能力考试种类'),
            blank=True,
            null=True,
            default=0,
            choices=ENGLISH_BAND_CHOICES,
            )
    english_band_score = models.IntegerField(
            _('英语能力考试分数'),
            blank=True,
            null=True,
            default=0,
            )

    hobby = models.CharField(
            _('兴趣爱好'),
            max_length=128,
            blank=True,
            default='',
            )

    # for the health condition field, we assume that no text here
    # means healthy
    health = models.CharField(
            _('健康状况'),
            max_length=64,
            blank=True,
            default='',
            )

    def __unicode__(self):
        return '%s (%s) 的信息' % (
                self.user.profile.realname,
                self.user.username,
                )

    def get_completeness(self):
        # calculate percentage of completeness...
        count = sum(
                1 if len(getattr(self, field_name)) > 0 else 0
                for field_name in _EFF_FIELDS
                )

        # true division
        return (count / _EFF_FIELDS_COUNT) * 100.0

    def get_username(self):
        return self.user.username
    get_username.short_description = _('用户名')

    def get_realname(self):
        return self.user.profile.realname
    # TODO: sync this w/ model field's verbose_name to adhere to DRY!!!
    get_realname.short_description = _('姓名')

    def get_id_number(self):
        return self.user.profile.id_number
    get_id_number.short_description = _('学号')

    def get_year(self):
        return self.klass.date.year


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
