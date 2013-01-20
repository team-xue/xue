# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from .models import *
from django.contrib import admin


class ExportTemplateAdmin(admin.ModelAdmin):
    list_display = (
            'title',
            'content_type',
            'identifier',
            )


admin.site.register(ExportTemplate, ExportTemplateAdmin)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8
