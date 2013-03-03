# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from django.db import models
from django.contrib.auth.models import User

_ = lambda x: x

from xue.common.choices import APPLICATION_STATUS_CHOICES, APPLICATION_STATUS_DICT


class TutorProject(models.Model):
    class Meta:
        verbose_name = _('导师项目')
        verbose_name_plural = _('导师项目')

    teacher = models.ForeignKey(User, verbose_name='教师', null=True)
    name = models.CharField('项目名称', unique=True, max_length=64)
    desc = models.CharField('简要介绍', max_length=500)
    requirements = models.CharField('对学生的要求', max_length=256)
    year = models.IntegerField('面向年份')

    def __unicode__(self):
        return '导师项目: %s' % (self.name, )

    def get_teacher_name(self):
        return self.teacher.profile.realname
    get_teacher_name.short_description = _('教师姓名')


class StudentProject(models.Model):
    class Meta:
        verbose_name = _('学生项目')
        verbose_name_plural = _('学生项目')

    student = models.ForeignKey(User)
    project = models.ForeignKey(TutorProject)
    status = models.IntegerField('申请状态', choices=APPLICATION_STATUS_CHOICES,
                                 default=0,
                                 )
    fail_reason = models.CharField('未通过原因', max_length=128, blank=True,
                                   default='', help_text='最多 128 字',
                                   )
    fail_count = models.IntegerField('被拒绝次数', default=0)
    # XXX tutor advice not currently built in...

    def __unicode__(self):
        return '%s (项目 %s)' % (
                self.student.profile.realname,
                self.project.name,
                )


class StudentApplication(models.Model):
    class Meta:
        verbose_name = _('学生申请')
        verbose_name_plural = _('学生申请')

    student = models.ForeignKey(User, verbose_name='学生', unique=True, )
    desc = models.TextField('申请理由', help_text='至少 200 字')
    status = models.IntegerField('申请状态', choices=APPLICATION_STATUS_CHOICES,
                                 default=0,
                                 )
    fail_reason = models.CharField('未通过原因', max_length=128, blank=True,
                                   default='', help_text='最多 128 字',
                                   )

    def __unicode__(self):
        return '%s 的申请' % (self.student.profile.realname, )


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
