# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .ethnic import ETHNIC_CHOICES


ROLE_CHOICES = (
     (0, u'学生'),
     (1, u'教师'),
     (2, u'程序'),
    )

POLITICAL_BKGND_CHOICES = (
     (0, u'群众'),
     (1, u'共青团员'),
     (2, u'中共预备党员'),
     (3, u'中共党员'),
     (4, u'民主党派人士'),
     (5, u'无党派人士'),
     (6, u'其他'),
    )

GENDER_CHOICES = (
     (0, u'无'),
     (1, u'女'),
     (2, u'男'),
    )

ENGLISH_BAND_CHOICES = (
                        (0, u'无'),
                        (4, u'英语四级'),
                        (6, u'英语六级'),
                        )

BAND_CHOICES = (
        (1, 'CET-4'),
        (2, 'CET-6'),
        (3, '校英语四级'),
        (4, '英语专业四级'),
        (5, '英语专业八级'),
        )

APPLICATION_STATUS_CHOICES = (
         (0, u'待处理'),
         (1, u'已通过'),
         (2, u'未通过'),
        )


curr_globals = globals()
for k, v in curr_globals.items():
    if k[-8:] == '_CHOICES':
        globals()['%s_DICT' % k[:-8]] = dict(v)
del curr_globals, k, v


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8:
