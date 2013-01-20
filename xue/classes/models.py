# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models


class Major(models.Model):
    class Meta:
        verbose_name = '专业'
        verbose_name_plural = '专业'

    name = models.CharField(u'专业名称', max_length=16)
    shortname = models.CharField(u'简称', max_length=4)
    code = models.CharField(u'专业代码', max_length=4)

    def __unicode__(self):
        return u'专业: %s %s (%s)' % (self.code, self.name, self.shortname, )


class LogicalClass(models.Model):
    class Meta:
        verbose_name = '逻辑班级'
        verbose_name_plural = '逻辑班级'

    date = models.DateField(u'入学日期')
    seq = models.IntegerField(u'班级号')
    major = models.ForeignKey(Major, verbose_name=u'专业')

    def __unicode__(self):
        return u'%s%02d%02d' % (
                self.major.shortname,
                self.date.year % 100,
                self.seq,
                )

    def get_class_code(self):
        return u'%s%02d%02d' % (
                self.major.code,
                self.date.year % 100,
                self.seq,
                )


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
