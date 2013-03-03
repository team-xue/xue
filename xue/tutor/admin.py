# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from xue.tutor.models import *
from django.contrib import admin


class TutorProjectAdmin(admin.ModelAdmin):
    list_display = (
            'get_teacher_name',
            'teacher',
            'name',
            'year',
            )

    list_filter = (
            'teacher__profile__realname',
            'year',
            )


class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = (
            'student',
            'get_student_realname',
            'get_student_year',
            'get_student_major',
            'get_student_klass',
            'get_student_political',
            'status',
            )

    list_filter = (
            'student__central_info__klass__date',
            'student__central_info__klass__major',
            'student__central_info__klass',
            'student__central_info__political',
            'status',
            )


admin.site.register(TutorProject, TutorProjectAdmin)
admin.site.register(StudentProject)
admin.site.register(StudentApplication, StudentApplicationAdmin)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8
