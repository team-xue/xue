# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division

from django.contrib import admin

from .models import *


class MaterialEntryAdmin(admin.ModelAdmin):
    list_display = (
            'get_realname',
            'get_username',
            'title',
            'is_locked',
            'get_length',
            )


admin.site.register(MaterialTag)
admin.site.register(MaterialEntry, MaterialEntryAdmin)


# vim:ai:et:ts=4:sw=4:sts=4:fenc=utf-8
