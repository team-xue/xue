# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from xue.common.choices import APPLICATION_STATUS_CHOICES, APPLICATION_STATUS_DICT


class TutorProject(models.Model):
    teacher = models.ForeignKey(User, verbose_name=u'教师', null=True)
    name = models.CharField(u'项目名称', unique=True, max_length=64)
    desc = models.CharField(u'简要介绍', max_length=500)
    requirements = models.CharField(u'对学生的要求', max_length=256)

    def __unicode__(self):
        return u'导师项目: %s' % (self.name, )


class StudentProject(models.Model):
    student = models.ForeignKey(User)
    project = models.ForeignKey(TutorProject)
    status = models.IntegerField(u'申请状态', choices=APPLICATION_STATUS_CHOICES,
                                 default=0,
                                 )
    fail_reason = models.CharField(u'未通过原因', max_length=128, blank=True,
                                   default=u'', help_text=u'最多 128 字',
                                   )
    fail_count = models.IntegerField(u'被拒绝次数', default=0)
    # XXX tutor advice not currently built in...

    def __unicode__(self):
        return u'%s (项目 %s)' % (
                self.student.profile.realname,
                self.project.name,
                )


class StudentApplication(models.Model):
    student = models.ForeignKey(User, verbose_name=u'学生', unique=True, )
    desc = models.TextField(u'申请理由', help_text=u'至少 200 字')
    status = models.IntegerField(u'申请状态', choices=APPLICATION_STATUS_CHOICES,
                                 default=0,
                                 )
    fail_reason = models.CharField(u'未通过原因', max_length=128, blank=True,
                                   default=u'', help_text=u'最多 128 字',
                                   )

    def __unicode__(self):
        return u'%s 的申请' % (self.student.profile.realname, )


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
