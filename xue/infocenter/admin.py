# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .models import *
from django.contrib import admin


if 0:
    # Damn, this functionality doesn't exist in Django 1.3...
    class SmartEthnicListFilter(admin.SimpleListFilter):
        title = '民族'
        parameter_name = 'ethnic'

        def lookups(self, request, model_admin):
            from ..common.choices import ETHNIC_CHOICES
            qs = model_admin.queryset(request)

            for val, name in ETHNIC_CHOICES:
                if qs.filter(ethnic=val).exists():
                    yield (val, name, )

        def queryset(self, request, queryset):
            return queryset.filter(ethnic=self.value())


class CentralStudentInfoAdmin(admin.ModelAdmin):
    list_display = (
            'get_realname',
            'get_username',
            'get_id_number',
            'ident',
            'phone',
            'klass',
            'political',
            'ethnic',
            'is_locked',
            )

    list_filter = (
            'klass',
            #SmartEthnicListFilter,
            'political',
            'english_band_type',
            )

    readonly_fields = (
            'join_date',
            )


admin.site.register(CentralStudentInfo, CentralStudentInfoAdmin)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8
