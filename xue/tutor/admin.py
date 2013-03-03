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

    list_filters = (
            'get_teacher_name',
            'year',
            )


admin.site.register(TutorProject, TutorProjectAdmin)
admin.site.register(StudentProject)
admin.site.register(StudentApplication)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8
