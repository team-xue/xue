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
            'year',
            )


class StudentProjectAdmin(admin.ModelAdmin):
    list_display = (
            'get_student_realname',
            'student',
            'status',
            'get_project_year',
            'project',
            'get_student_klass',
            'get_project_teacher_realname',
            'fail_count',
            )

    list_filter = (
            'status',
            'student__central_info__klass__major',
            'student__central_info__klass',
            )


class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = (
            'get_student_realname',
            'student',
            'status',
            'get_student_year',
            'get_student_major',
            'get_student_klass',
            'get_student_political',
            )

    list_filter = (
            'status',
            'student__central_info__klass__major',
            'student__central_info__political',
            'student__central_info__klass',
            )


admin.site.register(TutorProject, TutorProjectAdmin)
admin.site.register(StudentProject, StudentProjectAdmin)
admin.site.register(StudentApplication, StudentApplicationAdmin)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8
