# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

POVERTY_STATUS_CHOICES = (
        (u'PK', u'贫困'),
        (u'TK', u'特困'),
        )

AID_CHOICES = (
               (1, u'一等'),
               (2, u'二等'),
               )

# Create your models here.
class ApplicationEntry(models.Model):
    student = models.OneToOneField(User,
                                   unique=True,
                                   verbose_name=u'用户',
                                   )
    ctime = models.DateTimeField(u'申请日期', auto_now_add=True,
                                 editable=False, blank=True
                                 )
    mtime = models.DateTimeField(u'申请最后修改日期', auto_now=True,
                                 editable=False, blank=True
                                 )
    poverty_status = models.CharField(u'贫困状态', max_length=2,
                                      choices=POVERTY_STATUS_CHOICES
                                      )
    is_applied_loan = models.BooleanField(u'是否申请助学贷款')
    scholarship_lvl = models.IntegerField(u'10~11学年综合奖学金等级')
    overall_rank = models.IntegerField(u'综合测评班级内名次')
    aid_apply_for = models.IntegerField(u'申请国家助学金等级', choices=AID_CHOICES)
    cee_score_pastline = models.IntegerField(u'高考成绩高出省控线分数（新生填）', blank=True)
    application_text = models.TextField(u'申请理由')

    def __unicode__(self):
        return u'%s 的申请表' % self.student.profile.realname


# vim:set ai et ts=4 sw=4 sts=4 fenc=utf-8:
