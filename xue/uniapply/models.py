# -*- coding: utf-8 -*-

from __future__ import unicode_literals

__all__ = [
        'Target',
        'AuditingRule',
        'UniApplicationEntry',
        'AuditOutcome',
        ]

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _u
_ = lambda x: x

from ..common import choices
from ..classes.models import LogicalClass
from ..materials.models import MaterialEntry
from ..impexp.models import ExportTemplate


# "事项" or "item", the thing that is applied to by users
# for code clarity, it's named "target" instead, as "item" can mean
# a number of other things.
class Target(models.Model):
    class Meta:
        verbose_name = _('可申请事项')
        verbose_name_plural = _('可申请事项')

    # basic info, this is the ONLY easy part...
    user = models.ForeignKey(User, verbose_name=_('创建者'))
    name = models.CharField(_('事项名称'), max_length=128)
    desc = models.TextField(_('事项描述'), blank=True)
    pagelink = models.CharField(_('相关链接'), max_length=256, blank=True)

    # various access control things...
    start_date = models.DateTimeField(_('开始时间'))
    end_date = models.DateTimeField(_('结束时间'))
    allowed_classes = models.ManyToManyField(
            LogicalClass,
            verbose_name=_('适用班级'),
            )

    # internal dispatching logic
    identifier = models.CharField(
            _('内部代号'),
            max_length=128,
            unique=True,
            )

    # allow different targets to share an export template
    template = models.ForeignKey(ExportTemplate, verbose_name=_('导出模版'))

    def __unicode__(self):
        return '[申请事项: %s]' % (self.name, )


# 审核标准
class AuditingRule(models.Model):
    class Meta:
        verbose_name = _('审核标准')
        verbose_name_plural = _('审核标准')

    target = models.ForeignKey(Target, verbose_name=_('关联事项'))
    auditer = models.ForeignKey(User, verbose_name=_('审核负责人'))

    # priority-like, but rules with smaller "priorities" come first, so
    # the term "niceness" is appropriate
    niceness = models.IntegerField(_('审核层序数'))

    def __unicode__(self):
        return ('<[%(tgt)s]: 由 %(person)s (%(user)s)'
                ' 进行第 %(nice)d 审>') % {
                'tgt': self.target.name,
                'person': self.auditer.profile.realname,
                'user': self.auditer.username,
                'nice': self.niceness,
                }


# 统一格式申请条目
class UniApplicationEntry(models.Model):
    class Meta:
        verbose_name = _('申请条目')
        verbose_name_plural = _('申请条目')

        unique_together = (
                ('user', 'target', ),
                )

    user = models.ForeignKey(User, verbose_name=_('申请者'))
    target = models.ForeignKey(Target, verbose_name=_('所申请事项'))
    ctime = models.DateTimeField(_('申请日期'), auto_now_add=True)

    materials = models.ManyToManyField(
            MaterialEntry,
            verbose_name=_('关联材料'),
            )

    def __unicode__(self):
        return '<%(name)s (%(user)s) 申请 [%(target)s] 的条目>' % {
                'name': self.user.profile.realname,
                'user': self.user.username,
                'target': self.get_target_name(),
                }

    def get_target_name(self):
        return self.target.name
    get_target_name.short_description = _('事项标题')


#审核结果
class AuditOutcome(models.Model):
    class Meta:
        verbose_name = _('审核结果条目')
        verbose_name_plural = _('审核结果条目')

    entry = models.ForeignKey(UniApplicationEntry)
    rule = models.ForeignKey(AuditingRule)
    status = models.IntegerField(_('状态'), choices=choices.APPLICATION_STATUS_CHOICES, default=1)
    reason = models.CharField(_('原因'), max_length=256)

    # let's NOT define __unicode__ for this... combined w/ the rule object's
    # representation the resulting string would be WAY TOO LONG


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
