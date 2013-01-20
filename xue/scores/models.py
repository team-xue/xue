# -*- coding: utf-8 -*-

from django.db import models

from django.contrib.auth.models import User


class RawGradeEntry(models.Model):
    class Meta:
        verbose_name = '原始成绩条目'
        verbose_name_plural = '原始成绩条目'

    id_number = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    term = models.PositiveIntegerField()
    gpa = models.FloatField(blank=True)
    rawscore = models.FloatField(blank=True)

    def __unicode__(self):
        return u'%s 在 %d-%d 学年第 %d 学期的原始成绩: GPA %.03f [%.03f 分]' % (
                self.id_number,
                self.year,
                self.year + 1,
                self.term,
                self.gpa,
                self.rawscore,
                )


class GradeEntry(models.Model):
    class Meta:
        verbose_name = '成绩条目'
        verbose_name_plural = '成绩条目'

    student = models.ForeignKey(User, verbose_name=u'对应学生')

    year = models.PositiveIntegerField(u'学年')
    term = models.PositiveIntegerField(u'学期')
    gpa = models.FloatField(u'绩点')
    rawscore = models.FloatField(u'原始成绩', blank=True)

    def __unicode__(self):
        return u'成绩: %s %d-%d-%d学期 %.3f [%.2f]' % (
                self.student.profile.realname,
                self.year,
                self.year + 1,
                self.term,
                self.gpa,
                self.rawscore,
                )

    def gpa_from_raw(self):
        raw = self.rawscore

        if raw < 60.0:
            return 0.0

        # 1 to 5
        return (raw - 60) / 10.0 + 1


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf8:
